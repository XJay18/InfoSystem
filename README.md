# InfoSystem
Database Practical Training Assignment

- Assignment Start Date: July 10<sup>th</sup>, 2019
- Group Members:

    Member|Github|Contrib|
    :---:|:---:|:---:
    Junyi Cao|[XJay18](https://github.com/XJay18)|Crawl the data from website, UI support
    Guokai Wu|[kyleWu12138](https://github.com/kyleWu12138)|Construction and maintenance of the database
    Yu Shi|[tsstony](https://github.com/tsstony)|UI support

- Assignment Tasks:
    - [x] **Basic Requirements:** crawling the following web site academic report lecture notification.
        - http://www2.scut.edu.cn/sse/xshd/list1.htm
        - http://cs.scut.edu.cn/newcs/xygk/xytz/index.html
        - https://xxxy2016.jnu.edu.cn/Category_37/Index_1.aspx
        - http://info.scau.edu.cn/3762/list1.htm
        - http://eecs.pku.edu.cn/xygk1/jzxx1.htm
        - http://iiis.tsinghua.edu.cn/list-265-1.html
        - http://sklois.iie.cas.cn/xwzx/xshd/index.html
        - http://www.cs.sjtu.edu.cn/NewNotice.aspx
    - [x] **Filtering Requirements:** capturing only academic report information related to *information security* and *cryptography*.
    - [x] **Expansion Requirements:** be able to add new web addresses.
    - [x] **Display Requirements:** 
        - [x] providing the following information:
            > Lecture title, presenter, time, place, university, full text notification link
            
        - [x] providing at least 2 ways of time sorting. Sort by holding time. Sort by issued time.
             
        - [x] displaying the latest month's bulletin.

- Modules Used
    - [Scrapy](https://scrapy.org/)
    - [tkinter](https://docs.python.org/3/library/tkinter.html#)
    - [Boson Nlp](https://bosonnlp.com/) API
    - [Baidu Cloud](https://cloud.baidu.com/) API
    - more ...
    
- Usage
    1. Download via `git clone https://github.com/XJay18/InfoSystem.git`.
    2. Run the script in shell `bash deploy.sh`.
    3. Run the script in shell `bash app.sh`.
