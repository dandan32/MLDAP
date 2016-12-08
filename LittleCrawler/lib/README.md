## HTTP request 对象具有以下属性

    { 
        "url":"http://www.baidu.com", *
        "method":"GET",               *
        "data":"",                    *
        "user_agent":"",
        "headers": {},
        "cookies":{},
        "timeout":10,//(秒)
        "save":"123",
        "js":False,
        "load_images": false,
        "load_css":true
        "wait_before_end": 1, //(秒)
        "js_view_width": 1024,
        "js_view_height": 768,
        "js_script":"function(){return 1;}",
        "js_run_at":"document-start",// 默认为载入页面结束执行
        "clear_cookies":false,

    }


## HTTP response 对象具有以下对象  

    {
        "status_code": "status || 599 int",
        "ok":"True if status_code is 200",
        "error": "error message string",
        "url": "request url(maybe redirect) string",
      	"origin_url": "url string",
        "headers": "response headers dict{}",
        "cookies": "page cookie dict{}",
        "encoding":"encoding of response",
        "text": "Content of response, in unicode"
        "content":  "page content,in bytes",
        "etree": "the lxml element tree object",
        "doc":"a pyquery object",
        "time": "getting time cost(s)",
        "js_script_result": "js_script return",
        "save": "what you save in you request object"
        "request_data":"the request data"
    }