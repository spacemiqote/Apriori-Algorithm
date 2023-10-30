使用說明與範例：  
選擇實作的探勘關聯規則演算法：  
	Apriori 演算法  
1.  
	apriori.py 是我的作業  
	python apriori.py input_data.txt 0.5 0.7  
>		第一個參數為交易資料檔名
>		第二個參數為最小支持度
>		第三個參數為最小自信度

 執行後，將在文件夾內產生output_rules.txt  
	裡面就是關聯規則  
2.  
	checker.py 是檢查正確性的腳本(非作業，需額外安裝(efficient-apriori) `pip install efficient-apriori`)  
	python checker.py input_data.txt 0.5 0.7 output_rules.txt  
>		第一個參數為交易資料檔名
>		第二個參數是使用apriori.py生成output_rules時，我們使用的最小支持度
>		第三個參數是使用apriori.py生成output_rules時，我們使用的最小信賴度
>		第四個參數是我們要檢驗的output_rules.txt(apriori.py生成的關聯規則)

 執行後，假如不吻合皆為0，就沒有問題，若有則會打印出不吻合的規則。  
