from Common.CONST_j import CONST
from Common.Excel_x import Excel
from Common.WebPage import WebPage
from Common.Report import *
from Common.Alias import *
from pathlib import Path
import unittest


class TC2(unittest.TestCase):
    def __init__(self, testname, reportpath, browser="Firefox", Datasetrange="All"):
        self.caseno = 2
        exec("super(TC%d, self).__init__(testname)" % self.caseno)

        self.reportfilepath = reportpath
        self.Rowrange = Datasetrange
        self.browser = browser

    def setUp(self):

        self.excel = Excel(CONST.EXCELPATH)
        self.excel.Select_Sheet_By_Name(str(self.caseno))
        self.report = Excel(self.reportfilepath)
        self.casedirpath = Path(self.reportfilepath).parent / Path("TC%d" % self.caseno)
        self.stepsdirpath = self.casedirpath / Path("Steps")

        if not self.casedirpath.is_dir():
            self.casedirpath.mkdir()

        if not self.stepsdirpath.is_dir():
            self.stepsdirpath.mkdir()


    def test_Excute(self):

        for i in self.excel.Get_Excution_DataSet("executed"):
            try:
                bro = self.excel.Get_Value_By_ColName("Browser", i)
                if bro is not None:
                    self.browser = bro

                self.page = WebPage()
                self.driver = self.page.Start_Up(CONST.URL, self.browser)

                self.page.Log_in(self.excel, self.caseno, i, self.casedirpath)

                if self.page.Verify_Text(self.excel.Get_Value_By_ColName("Assertion", i),
                                         LoginPageAlias_CSS['Login_Error_Prompt']):
                    Log("success", self.caseno, i, self.casedirpath)
                else:
                    raise AssertionError("The element not contains the Assertion text")

            except Exception as msg:
                Log(str(msg), self.caseno, i, self.casedirpath)

                Generate_Report(self.driver, self.excel, self.report, "fail", self.caseno, self.casedirpath, i)

                self.driver.quit()

            else:

                Generate_Report(self.driver, self.excel, self.report, "pass", self.caseno, self.casedirpath, i)
                self.driver.quit()

    def tearDown(self):
        self.report.Save_Excel()
        self.excel = Excel(self.reportfilepath)
        self.excel.Select_Sheet_By_Name(str(self.caseno))
        # print(self.excel)
        Generate_Final_Report(self.excel, self.report, self.caseno)
        self.report.Save_Excel()



