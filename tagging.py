__author__ = 'Tamir'

import pymongo
import wx
import wx.lib.scrolledpanel
import wx.lib.agw.aquabutton as ab

if __name__ == '__main__':
    class MainFrame(wx.Frame):
        def __init__(self):
            #initialize the main frame
            wx.Frame.__init__(self, None, -1, title="Tagging", size=wx.DisplaySize())
            self.panel = wx.Panel(self, size=self.GetSize())
            self.panel.SetBackgroundColour('#dfe3ee')

            self.title_pic = wx.Image('Title.JPG', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
            self.pic = wx.StaticBitmap(self, -1, self.title_pic)
            self.__set_title()

            self.number_file = open("number.txt", 'r')
            self.code_id = self.number_file.read()
            self.number_file.close()

            self.doc_code_panel = wx.Panel(self.panel, pos=(100, 150), size=(500, 496), style=wx.SUNKEN_BORDER,
                                           id=int(self.code_id))
            self.doc_code = wx.StaticText(self.doc_code_panel, pos=(5, 5))
            self.__set_starting_code()

            self.queries_panel = wx.lib.scrolledpanel.ScrolledPanel(self.panel, pos=(675, 150), size=(600, 496),
                                                                    style=wx.SUNKEN_BORDER)
            self.__set_queries()

            button = ab.AquaButton(self.panel, label="next", pos=(616, 600))
            button.DoGetBestSize()
            button.SetBackgroundColour('#0000CD')
            button.SetForegroundColour('#FFFFF0')
            button.SetHoverColour('#008B00')
            button.Bind(wx.EVT_BUTTON, self.foo)

        def foo(self, a):
            """
            This function insert to the collection 'tagged' the query for the current main code according to the
                clicked panels
            """
            record = {'code': self.doc_code.GetLabel(), 'code_id': self.code_id}
            for lab in self.queries_panel.GetChildren()[0].GetChildren():
                if lab.GetBackgroundColour() == '#dfe3ee':
                    tag = '0'
                else:
                    tag = '1'
                record[str('code_' + str(lab.GetId()))] = tag
                lab.SetBackgroundColour('#dfe3ee')
                lab.Refresh()
            results.insert(record)
            self.code_id = str(int(self.code_id) + 1)
            self.number_file = open("number.txt", 'w')
            self.number_file.write(self.code_id)
            self.number_file.close()
            if documents.count() <= int(self.code_id):
                self.doc_code.SetLabel("FINISHED!! :-)")
            else:
                self.doc_code.SetLabel(documents.find({"code_id": self.code_id})[0]['code'])

        def __set_title(self):
            self.pic.SetPosition((200, 5))

        def __set_starting_code(self):
            """
            initialize the main code according to the last one we've tagged
            """
            self.doc_code_panel.Show()
            if int(self.code_id) >= documents.count():
                code = "FINISHED! :-)"
            else:
                code = documents.find({"code_id": self.code_id})[0]['code']
            self.doc_code.SetLabel(code)
            self.doc_code.SetId(int(self.code_id))
            self.doc_code.Show()

        def __set_queries(self):
            """
            show all the 55 code-queries
            """
            self.queries_panel.Show()
            self.queries_panel.SetupScrolling()
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer_panel = wx.Panel(self.queries_panel, size=(600, 7230))
            query_panel = []
            for query in queries.find():
                if len(query_panel) == 0:
                    upper = 10
                else:
                    upper = query_panel[len(query_panel) - 1].GetSize()[1] + \
                            query_panel[len(query_panel) - 1].GetPosition()[1] + 10
                temp_panel = wx.Panel(sizer_panel, pos=(10, upper), size=(100, 30), style=wx.SIMPLE_BORDER,
                                      id=query['code_id'])
                query_panel.append(temp_panel)
                temp_panel.SetBackgroundColour('#dfe3ee')
                temp_panel.Show()
                query_code = wx.StaticText(temp_panel, pos=(5, 5), label=query['code'], id=query['code_id'])
                temp_panel.SetInitialSize()
                temp_panel.Bind(wx.EVT_LEFT_DOWN, self.__get_select(temp_panel))
                query_code.Bind(wx.EVT_LEFT_DOWN, self.__get_select(temp_panel))
                self.queries_panel.FitInside()
            sizer.Add(sizer_panel, wx.FIXED_MINSIZE, 0)
            self.queries_panel.SetSizer(sizer)

        def __get_select(self, clicked_panel):
            """
            change the background color of a clicked panel
            """
            def __select(self):
                if clicked_panel.GetBackgroundColour() == '#dfe3ee':
                    clicked_panel.SetBackgroundColour('#F7A67D')
                else:
                    clicked_panel.SetBackgroundColour('#dfe3ee')
                clicked_panel.Refresh()

            return __select

    client = pymongo.MongoClient()
    db = client.dataset
    documents = db.all_queries
    queries = db.test_queries
    results = db.tagged

    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
    print "bye"
