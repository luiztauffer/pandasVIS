import pandas as pd
import numpy as np


def ts_bin_states(df, column):
    """
    Binning of states that last for several samples. Basically, it is a
    'state_changed' counter. E.g.:
    Index:     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
    State:     | a | a | a | a | b | b | b | a | a |
    State_bin: | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 2 | 2 |

    Parameters:
    -----------
    df : DataFrame
        Pandas DataFrame.
    column : str
        Name of column with states to be binned.

    Returns:
    -----------
    df : DataFrame
        Updated DataFrame
    """
    df[column+'_bin'] = 0
    states = list(df[column].unique())
    last_st = None
    st_bin = -1
    for index, row in df.iterrows():
        curr_st = row[column]
        if curr_st == last_st:
            df.loc[index,column+'_bin'] = st_bin
        else:
            st_bin += 1
            df.loc[index,column+'_bin'] = st_bin
            last_st = curr_st
    return df



def ts_states_df(df, states_column=None, states_bins_column=None,
                 vars_columns=None):
    """
    Create DataFrame of time varying discrete states as observations.

    Parameters:
    -----------
    df : DataFrame
        Pandas DataFrame.
    states_column : str
        Name of column with discrete states.
    states_bin_column : str, optional
        Name of column with states bins. If it is not passed, it will be calculated
        for states_column.
    vars_columns : list of str, optional
        List of strings with names of variables (df columns) of interest. If it
        is not passed, all columns from df are used.

    Returns:
    -----------
    df : DataFrame
        Updated DataFrame
    df_states : DataFrame
        DataFrame organized with states as observations. Columns are the same
        as df, except they are now lists of values with lengths relative to each
        states duration.
    """
    #Check if index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        print("DataFrame index should be of type DatetimeIndex.")
        return (df, None)

    #Check if state is categorical
    if not isinstance(df[states_column].dtype, pd.api.types.CategoricalDtype):
        print("DataFrame states column should be of type Category.")
        return (df, None)

    #Check passed arguments
    if states_bins_column is None:
        if states_column is None:
            print("You should provide either the column with states_bins or a "+
                  "column with time varying discrete states to be binned.")
            return (df, None)
        else:
            df = ts_bin_states(df=df, column=states_column)
            states_bins_column = states_column + '_bin'

    #Variables of interest
    if vars_columns is None:
        vars_columns = df.columns.tolist()
        vars_columns.remove(states_column)
        vars_columns.remove(states_bins_column)

    #Initiate States DataFrame
    nStatesBins = df[states_bins_column].max()
    df_states = pd.DataFrame(data=np.empty((nStatesBins, len(vars_columns)))+np.nan,
                             columns=vars_columns,
                             dtype=object)
    df_states[states_column] = pd.Categorical(values=np.zeros(nStatesBins, dtype='int'),
                                              categories=df[states_column].unique().to_list())
    df_states['duration_samples'] = np.zeros(nStatesBins, dtype='int')
    df_states['duration_time'] = np.zeros(nStatesBins)

    #Iterate over states and fill DataFrame
    for stind in range(nStatesBins):
        df_aux = df.loc[df[states_bins_column]==stind]
        df_states.at[stind, states_column] = df_aux.iloc[0][states_column]
        duration = df_aux.shape[0]
        df_states.at[stind, 'duration_samples'] = duration
        df_states.at[stind, 'duration_time'] = df_aux.index[-1]-df_aux.index[0]
        for var in vars_columns:
            df_states.at[stind, var] = df_aux[var].to_list()

    return (df, df_states)
