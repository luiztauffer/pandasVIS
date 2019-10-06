from ipywidgets import widgets, HBox, VBox, GridspecLayout


class DashBoard(VBox):
    def __init__(self, fig):
        super().__init__()
        self.fig = fig
        self.nSubs = sum(['xaxis' in i for i in fig['layout']])

        # Layout control widgets
        field_lay = widgets.Layout(max_height='40px', max_width='120px',
            min_height='30px', min_width='70px')
        fonts_names = ["Arial", "Balto", "Courier New", "Droid Sans",
                     "Droid Serif", "Droid Sans Mono", "Gravitas One",
                     "Old Standard TT", "Open Sans", "Overpass",
                     "PT Sans Narrow", "Raleway", "Times New Roman"]
        fonts_list = [(fnt, i+1) for i, fnt in enumerate(fonts_names)]
        tickoptions_names = ['inside', 'outside', '']
        tickoptions_list = [(v, i+1) for i, v in enumerate(tickoptions_names)]

        # General --------------------------------------------------------------
        chk_general_autosize = widgets.Checkbox(
            value=fig.layout.autosize, description='Autosize')
        self.txt_gen_width = widgets.FloatText(value=fig.layout.width, layout=field_lay)
        self.txt_gen_height = widgets.FloatText(value=fig.layout.height, layout=field_lay)
        hb_dims = HBox([widgets.Label('width/height:'), self.txt_gen_width, self.txt_gen_height])

        txt_fontsize = widgets.FloatText(value=fig.layout.font.size, layout=field_lay)
        drd_fontfamily = widgets.Dropdown(
            options=fonts_list, layout=field_lay,
            value=fonts_names.index(fig.layout.font.family)+1)
        drd_fontfamily.observe(self.set_gen_fontfamily, names='label')
        clr_font = widgets.ColorPicker(concise=True, value=fig.layout.font.color)
        hb_font = HBox([widgets.Label('font:'), txt_fontsize, drd_fontfamily, clr_font])

        clr_paperbg = widgets.ColorPicker(layout=field_lay,
            concise=True, value=fig.layout.paper_bgcolor,  description='paper_bgcolor')
        clr_plotbg = widgets.ColorPicker(layout=field_lay,
            concise=True, value=fig.layout.plot_bgcolor,  description='plot_bgcolor')
        hb_colorbg = HBox([clr_paperbg, clr_plotbg])

        drd_hovermode = widgets.Dropdown(
            options=[('Closest', 1), ('x', 2), ('y', 3), ('False', 4)],
            value=1, layout=field_lay)
        drd_hovermode.observe(self.set_gen_hovermode, names='label')
        hb_hovermode = HBox([widgets.Label('hovermode:'), drd_hovermode])

        vb_general = VBox([chk_general_autosize, hb_dims, hb_font,
                           hb_colorbg, hb_hovermode])
        controls_general = {
            'autosize': chk_general_autosize,
            'width': self.txt_gen_width,
            'height': self.txt_gen_height,
            'fontsize': txt_fontsize,
            'fontcolor': clr_font,
            'paperbgcolor': clr_paperbg,
            'plotbgcolor': clr_plotbg,
        }
        widgets.interactive_output(self.set_general, controls_general)


        # Title ----------------------------------------------------------------
        txt_titletext = widgets.Text(value=fig.layout.title.text, description='Text:')
        txt_titlefontsize = widgets.FloatText(value=fig.layout.titlefont.size, layout=field_lay)
        drd_titlefontfamily = widgets.Dropdown(
            options=fonts_list, layout=field_lay,
            value=fonts_names.index(fig.layout.titlefont.family)+1)
        drd_titlefontfamily.observe(self.set_gen_titlefontfamily, names='label')
        clr_titlefont = widgets.ColorPicker(concise=True, value=fig.layout.titlefont.color)
        hb_title = HBox([widgets.Label('font:'), txt_titlefontsize,
                         drd_titlefontfamily, clr_titlefont])
        vb_title = VBox([txt_titletext, hb_title])
        controls = {
            'title_text': txt_titletext,
            'title_fontsize': txt_titlefontsize,
            'title_fontcolor': clr_titlefont,
        }
        widgets.interactive_output(self.set_title, controls)

        # X axis ---------------------------------------------------------------
        chk_xaxis_visible = widgets.Checkbox(
            value=fig.layout.xaxis.visible, description='Visible')
        clr_xaxis = widgets.ColorPicker(concise=True, value=fig.layout.xaxis.color)
        hb0_xaxis = HBox([chk_xaxis_visible, clr_xaxis])

        txt_xaxis_fontsize = widgets.FloatText(value=fig.layout.xaxis.titlefont.size, layout=field_lay)
        drd_xaxis_fontfamily = widgets.Dropdown(
            options=fonts_list, layout=field_lay,
            value=fonts_names.index(fig.layout.xaxis.titlefont.family)+1)
        drd_xaxis_fontfamily.observe(self.set_xaxis_titlefontfamily, names='label')
        clr_xaxis_font = widgets.ColorPicker(concise=True, value=fig.layout.xaxis.titlefont.color)
        hb1_xaxis = HBox([widgets.Label('font:'), txt_xaxis_fontsize,
                          drd_xaxis_fontfamily, clr_xaxis_font])

        drd_xaxis_ticks = widgets.Dropdown(
            options=tickoptions_list, layout=field_lay,
            value=tickoptions_names.index(fig.layout.xaxis.ticks)+1)
        drd_xaxis_ticks.observe(self.set_xaxis_ticks, names='label')
        txt_xaxis_nticks = widgets.IntText(value=fig.layout.xaxis.nticks, layout=field_lay)
        hb2_xaxis = HBox([widgets.Label('ticks:'), drd_xaxis_ticks, txt_xaxis_nticks])

        txt_xaxis_ticklen = widgets.FloatText(value=fig.layout.xaxis.ticklen, layout=field_lay)
        txt_xaxis_tickwid = widgets.FloatText(value=fig.layout.xaxis.tickwidth, layout=field_lay)
        clr_xaxis_tick = widgets.ColorPicker(concise=True, value=fig.layout.xaxis.tickcolor)
        hb3_xaxis = HBox([widgets.Label('ticks len/wid:'), txt_xaxis_ticklen,
                          txt_xaxis_tickwid, clr_xaxis_tick])

        chk_xaxis_showticklabels = widgets.Checkbox(
            value=fig.layout.xaxis.showticklabels, description='Show tick labels')
        chk_xaxis_tickangle = widgets.Checkbox(
            value=not isinstance(fig.layout.xaxis.tickangle, (int, float)), description='auto')
        self.txt_xaxis_tickangle = widgets.FloatText(
            value=fig.layout.xaxis.tickangle if fig.layout.xaxis.tickangle != 'auto' else 0,
            layout=field_lay)
        hb4_xaxis = HBox([widgets.Label('ticks angle:'), chk_xaxis_tickangle,
                          self.txt_xaxis_tickangle])


        vb_xaxis = VBox([hb0_xaxis, hb1_xaxis, hb2_xaxis, hb3_xaxis,
                         chk_xaxis_showticklabels, hb4_xaxis])

        xaxis_controls = {
            'visible': chk_xaxis_visible,
            'color': clr_xaxis,
            'title_fontsize': txt_xaxis_fontsize,
            'title_fontcolor': clr_xaxis_font,
            'nticks': txt_xaxis_nticks,
            'ticklen': txt_xaxis_ticklen,
            'tickwid': txt_xaxis_tickwid,
            'tickcolor': clr_xaxis_tick,
            'showticklabels': chk_xaxis_showticklabels,
            'tickangleauto': chk_xaxis_tickangle,
            'tickangle': self.txt_xaxis_tickangle,
        }
        widgets.interactive_output(self.set_xaxis, xaxis_controls)

        # Y axis ---------------------------------------------------------------
        chk_yaxis_visible = widgets.Checkbox(
            value=fig.layout.yaxis.visible, description='Visible')
        clr_yaxis = widgets.ColorPicker(concise=True, value=fig.layout.yaxis.color)
        hb0_yaxis = HBox([chk_yaxis_visible, clr_yaxis])

        txt_yaxis_fontsize = widgets.FloatText(value=fig.layout.yaxis.titlefont.size, layout=field_lay)
        drd_yaxis_fontfamily = widgets.Dropdown(
            options=fonts_list, layout=field_lay,
            value=fonts_names.index(fig.layout.yaxis.titlefont.family)+1)
        drd_yaxis_fontfamily.observe(self.set_yaxis_titlefontfamily, names='label')
        clr_yaxis_font = widgets.ColorPicker(concise=True, value=fig.layout.yaxis.titlefont.color)
        hb1_yaxis = HBox([widgets.Label('font:'), txt_yaxis_fontsize,
                          drd_yaxis_fontfamily, clr_yaxis_font])

        drd_yaxis_ticks = widgets.Dropdown(
            options=tickoptions_list, layout=field_lay,
            value=tickoptions_names.index(fig.layout.yaxis.ticks)+1)
        drd_yaxis_ticks.observe(self.set_yaxis_ticks, names='label')
        txt_yaxis_nticks = widgets.IntText(value=fig.layout.yaxis.nticks, layout=field_lay)
        hb2_yaxis = HBox([widgets.Label('ticks:'), drd_yaxis_ticks, txt_yaxis_nticks])

        txt_yaxis_ticklen = widgets.FloatText(value=fig.layout.yaxis.ticklen, layout=field_lay)
        txt_yaxis_tickwid = widgets.FloatText(value=fig.layout.yaxis.tickwidth, layout=field_lay)
        clr_yaxis_tick = widgets.ColorPicker(concise=True, value=fig.layout.yaxis.tickcolor)
        hb3_yaxis = HBox([widgets.Label('ticks len/wid:'), txt_yaxis_ticklen,
                          txt_yaxis_tickwid, clr_yaxis_tick])

        chk_yaxis_showticklabels = widgets.Checkbox(
            value=fig.layout.yaxis.showticklabels, description='Show tick labels')
        chk_yaxis_tickangle = widgets.Checkbox(
            value=not isinstance(fig.layout.yaxis.tickangle, (int, float)), description='auto')
        self.txt_yaxis_tickangle = widgets.FloatText(
            value=fig.layout.yaxis.tickangle if fig.layout.yaxis.tickangle != 'auto' else 0,
            layout=field_lay)
        hb4_yaxis = HBox([widgets.Label('ticks angle:'), chk_yaxis_tickangle,
                          self.txt_yaxis_tickangle])


        vb_yaxis = VBox([hb0_yaxis, hb1_yaxis, hb2_yaxis, hb3_yaxis,
                         chk_yaxis_showticklabels, hb4_yaxis])

        yaxis_controls = {
            'visible': chk_yaxis_visible,
            'color': clr_yaxis,
            'title_fontsize': txt_yaxis_fontsize,
            'title_fontcolor': clr_yaxis_font,
            'nticks': txt_yaxis_nticks,
            'ticklen': txt_yaxis_ticklen,
            'tickwid': txt_yaxis_tickwid,
            'tickcolor': clr_yaxis_tick,
            'showticklabels': chk_yaxis_showticklabels,
            'tickangleauto': chk_yaxis_tickangle,
            'tickangle': self.txt_yaxis_tickangle,
        }
        widgets.interactive_output(self.set_yaxis, yaxis_controls)

        # Export ---------------------------------------------------------------
        

        # Organize buttons layout ----------------------------------------------
        self.tab_nest = widgets.Tab()
        self.tab_nest.children = [vb_general, vb_title, vb_xaxis, vb_yaxis]
        self.tab_nest.set_title(0, 'General')
        self.tab_nest.set_title(1, 'Title')
        self.tab_nest.set_title(2, 'X axis')
        self.tab_nest.set_title(3, 'Y axis')

        acc_all = widgets.Accordion(
            children=[self.tab_nest],
            selected_index=None
        )
        acc_all.set_title(0, 'Edit layout')

        self.children = [acc_all, fig]

    def set_general(self, autosize, width, height, fontsize, fontcolor,
                    paperbgcolor, plotbgcolor):
        self.fig.layout.autosize = autosize
        if autosize:
            self.fig.layout.width = None
            self.fig.layout.height = None
            self.txt_gen_width.disabled = True
            self.txt_gen_height.disabled = True
        else:
            self.txt_gen_width.disabled = False
            self.txt_gen_height.disabled = False
            self.fig.layout.width = width
            self.fig.layout.height = height
        self.fig.layout.font.size = fontsize
        self.fig.layout.font.color = fontcolor
        self.fig.layout.paper_bgcolor = paperbgcolor
        self.fig.layout.plot_bgcolor = plotbgcolor

    def set_gen_fontfamily(self, change):
        self.fig.layout.font.family = change['new']

    def set_gen_hovermode(self, change):
        if change['new'] == 'False':
            self.fig.layout.hovermode = False
        else:
            self.fig.layout.hovermode = change['new']

    def set_title(self, title_text, title_fontsize, title_fontcolor):
        self.fig.layout.title.text = title_text
        self.fig.layout.titlefont.size = title_fontsize
        self.fig.layout.titlefont.color = title_fontcolor

    def set_gen_titlefontfamily(self, change):
        self.fig.layout.titlefont.family = change['new']

    def set_xaxis(self, visible, color, title_fontsize, title_fontcolor, nticks,
                  ticklen, tickwid, tickcolor, showticklabels, tickangleauto,
                  tickangle):
        for i in range(self.nSubs):
            xname = 'xaxis' if i == 0 else 'xaxis'+str(i)
            curr = getattr(self.fig.layout, xname)
            curr.visible = visible
            curr.color = color
            curr.titlefont.size = title_fontsize
            curr.titlefont.color = title_fontcolor
            curr.nticks = nticks
            curr.ticklen = ticklen
            curr.tickwidth = tickwid
            curr.tickcolor = tickcolor
            curr.showticklabels = showticklabels
            if tickangleauto:
                curr.tickangle = None
                self.txt_xaxis_tickangle.disabled = True
            else:
                self.txt_xaxis_tickangle.disabled = False
                curr.tickangle = self.txt_xaxis_tickangle.value

    def set_xaxis_titlefontfamily(self, change):
        for i in range(self.nSubs):
            xname = 'xaxis' if i == 0 else 'xaxis'+str(i)
            curr = getattr(self.fig.layout, xname)
            curr.titlefont.family = change['new']

    def set_xaxis_ticks(self, change):
        for i in range(self.nSubs):
            xname = 'xaxis' if i == 0 else 'xaxis'+str(i)
            curr = getattr(self.fig.layout, xname)
            curr.ticks = change['new']

    def set_yaxis(self, visible, color, title_fontsize, title_fontcolor, nticks,
                  ticklen, tickwid, tickcolor, showticklabels, tickangleauto,
                  tickangle):
        for i in range(self.nSubs):
            yname = 'yaxis' if i == 0 else 'yaxis'+str(i)
            curr = getattr(self.fig.layout, yname)
            curr.visible = visible
            curr.color = color
            curr.titlefont.size = title_fontsize
            curr.titlefont.color = title_fontcolor
            curr.nticks = nticks
            curr.ticklen = ticklen
            curr.tickwidth = tickwid
            curr.tickcolor = tickcolor
            curr.showticklabels = showticklabels
            if tickangleauto:
                curr.tickangle = None
                self.txt_yaxis_tickangle.disabled = True
            else:
                self.txt_yaxis_tickangle.disabled = False
                curr.tickangle = self.txt_yaxis_tickangle.value

    def set_yaxis_titlefontfamily(self, change):
        for i in range(self.nSubs):
            yname = 'yaxis' if i == 0 else 'yaxis'+str(i)
            curr = getattr(self.fig.layout, yname)
            curr.titlefont.family = change['new']

    def set_yaxis_ticks(self, change):
        for i in range(self.nSubs):
            yname = 'yaxis' if i == 0 else 'yaxis'+str(i)
            curr = getattr(self.fig.layout, yname)
            curr.ticks = change['new']
