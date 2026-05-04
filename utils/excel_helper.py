import openpyxl

class ExcelHelper:
    @staticmethod
    def get_data_from_testcase(file_path, sheet_name):
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook[sheet_name]
        
        test_cases = []
        
        for row in sheet.iter_rows(min_row=10, values_only=True):
            tc_id = row[0]     
            raw_data = row[3]   
            
            if not tc_id or not str(tc_id).startswith("TC_"):
                continue
                
            parsed_data = {}
            if raw_data:
                lines = str(raw_data).strip().split('\n')
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        parsed_data[key.strip()] = value.strip()
            
            test_cases.append({
                "id": tc_id,
                "data": parsed_data
            })
            
        return test_cases