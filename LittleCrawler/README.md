![LitteCrawler 爬虫架构](LittleCrawlerArchitecture.png)


Fetcher 参数

	{
        "js_view_width": 1024,
      	"js_view_height": 768,
        "headers": {},
      	"cookies":{},
        "load_images": false,
        "timeout":10,//(秒)
        "wait_before_end": 1, //(秒)
        "js_script":"function(){return 1;}",
        "js_run_at":"document-start",// 默认为载入页面结束执行
        "url":"http://www.baidu.com", *  
        "method":"GET",               *  
        "data":"",                    *
        "save":"123",                 
      	"clear_cookies":false,
      	"load_css":true
    }

