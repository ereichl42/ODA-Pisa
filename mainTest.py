# Test and try to import the module
#

from utils.load_PISA_data_fromExcel import load_PISA_data_fromExcel

if __name__ == "__main__":
    test = load_PISA_data_fromExcel(
        "data/pisa_data/original_xls_source_combined_tables/IDEExcelExport-Apr222024-0515PM.xls")


# Get project tree
# python -m pip install tree
# python -m tree -L 2
