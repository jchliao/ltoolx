from ltoolx.svg_utils import modify_line_path
from ltoolx.matplotlib_utils import *  # noqa: F403
from bs4 import Tag,BeautifulSoup
import unittest


class LtoolxTest(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()
    
    def test_my_modify_path(self):
        svg_content = """
        <path d="M 74.019678 190 
                        L 83.808506 125.526021 
                        L 104.318101 73.874339 
                        L 124.827695 65.022991 
                        L 145.337289 63.043574 
                        L 165.846884 60.466556 
                        L 186.356478 58.188417 
                        " clip-path="url(#pf37342d535)" style="fill: none; stroke: #ff0000; stroke-width: 0.75; stroke-linecap: square"/>
        """
        soup = BeautifulSoup(svg_content, 'xml')
        # print(soup)
        new_content = modify_line_path(soup)
        print(new_content.name)



if __name__ == "__main__":
    unittest.main() 
