class Utils:
    
    @staticmethod
    def xml_to_dict(element):
        
        """
        XML 데이터를 딕셔너리로 변환하는 함수

        Input: XML 데이터
        Returns: dict
        """
        result = {}
        for child in element:
            if child:
                result[child.tag] = Utils.xml_to_dict(child)
            else:
                result[child.tag] = child.text
        return result