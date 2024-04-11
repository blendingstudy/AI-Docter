import pandas as pd
from django.conf import settings
from googleapiclient.discovery import build


class SearchApi:
    Trash_Link = []

    def google_api(
            self,
            query: str,
            wanted_row: int = 3,
            **kwargs
    ) -> pd.DataFrame:
        """
        input : 
            query : str  검색하고 싶은 검색어 
            wanted_row : str 검색 결과를 몇 행 저장할 것인지 
        output : 
            df_google : dataframe / column = title, link,description  
            사용자로 부터 입력받은 쿼리문을 통해 나온 검색 결과를 wanted_row만큼 (100행을 입력받았으면) 100행이 저장된 데이터 프레임을 return합니다.
        """
        query = query.replace("|", "OR")  #쿼리에서 입력받은 | 기호를 OR 로 바꿉니다
        # query += "-filetype:pdf" # 검색식을 사용하여 file type이 pdf가 아닌 것을 제외시켰습니다 

        df_google = pd.DataFrame(
            columns=['Title', 'Link', 'Description'])  # df_Google이라는 데이터 프레임에 컬럼명은 Title, Link, Description으로 설정했습니다.

        row_count = 0  # dataframe에 정보가 입력되는 것을 카운트 하기 위해 만든 변수입니다.

        service = build("customsearch", "v1", developerKey=settings.GOOGLE_API_KEY)

        for start_page in range(1, wanted_row + 1000, 10):

            # 1페이지, 11페이지,21페이지 마다,             
            res = service.cse().list(q=query, cx=settings.GOOGLE_CSE_ID, start=start_page, **kwargs).execute()
            search_items = res["items"]
            # search_items엔 검색결과 [1~ 10]개의 아이템들이 담겨있다.  start_page = 11 ~ [11~20] 

            try:
                #try 구문을 하는 이유: 검색 결과가 null인 경우 link를 가져올 수가 없어서 없으면 없는대로 예외처리
                for search_item in search_items:
                    # link 가져오기 
                    link = search_item["link"]
                    # link url에 출처가 신뢰도가 낮은 사이트의 정보라면 데이터프레임에 저장하지 않고 넘어갑니다. 
                    if not any(trash in link for trash in self.Trash_Link):
                        # 제목저장
                        title = search_item["title"]

                        if title == "Untitled":
                            continue

                        # 설명 저장 
                        descripiton = search_item["snippet"]
                        # df_google에 한줄한줄 append 
                        df_google.loc[row_count] = [title, link, descripiton]
                        # 저장하면 행 갯수 카운트 
                        row_count += 1
                        if (row_count >= wanted_row) or (row_count == 300):
                            #원하는 갯수만큼 저장끝나면
                            return df_google
            except:
                # 더 이상 검색결과가 없으면 df_google 리턴 후 종료
                return df_google

        return df_google
