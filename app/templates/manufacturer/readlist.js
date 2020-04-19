var container = document.getElementById("container");
 
window.onload = function() {
    
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
 
        if(this.readyState == 4 && this.status == 200) {
            
            //读取JSON文件，把字符串转换为js对象
            var message = JSON.parse(this.responseText);
            
            //创建表元素
            var json_table = document.createElement("table");
            var json_tr = document.createElement("tr");
 
 
            //读取JSON文件中键的数量已经各键值的数量来创建表
 
            for(var key in message) {
 
                var json_th = document.createElement("th");
                
                //获取键名
                var th_txt = document.createTextNode(key);
 
                json_th.appendChild(th_txt);
                json_tr.appendChild(json_th);
                json_table.appendChild(json_tr);
                
                //修改表格样式
                json_th.style.border = "1px solid black";
 
               
            }
    
            for(var num in message.name) {
 
                var json_tr = document.createElement("tr");
                
 
                for(var key in message) {
                    var json_td = document.createElement("td");
                    var td_txt = document.createTextNode(message[key][num]);
                   
                    json_td.appendChild(td_txt);
                    json_tr.appendChild(json_td);
                    json_table.appendChild(json_tr);
 
                   
                    json_td.style.border = "1px solid black";
                
                    //计算点击次数
                    var count = 0;
 
                    //按单元格显示对应的名片
                    json_td.onclick = function() {
 
                        var txt = "";
                        count++;
 
                        for(var key in message) {
                           
                            txt += message[key][this.parentNode.rowIndex - 1] + "   ";
                           
                        }
 
                        //再次点击时删除之前的名片
                        if(count > 1) {
                            container.removeChild(document.getElementsByTagName("div")[1]);
                        }
                        
                        //创建名片
                        createCard(txt);
                         
                    }
                }
         
                
            }
   
            //添加表格
            container.appendChild(json_table);
          
            //改变表格样式
            json_table.style.border = "1px solid black";
            json_table.style.width = "800px";
            
        }
    };
 
    xmlhttp.open("GET", "json_table.txt", true);
    xmlhttp.send();
}
 
 
//创建卡片
var createCard = function(txt) {
 
    var card_page = document.createElement("div");
    var img = document.createElement("img");
    var introduce = document.createElement("p");
    var introduce_txt = document.createTextNode(txt);
 
    introduce.appendChild(introduce_txt);
    card_page.appendChild(img);
    card_page.appendChild(introduce);
    container.appendChild(card_page);
 
 
    card_page.style.backgroundColor = "#39b0fb";
    card_page.style.width = "400px";
    card_page.style.height = "250px";
    card_page.style.marginTop = "80px";
    card_page.style.marginLeft = "auto";
    card_page.style.marginRight = "auto";
    card_page.style.boxShadow = "10px 8px 5px #bababa ";
    
    img.src = "小黄人.png";
    img.style.width = "150px";
    img.style.height = "150px";
    img.style.cssFloat = "left";
    img.style.marginLeft = "10px";
    img.style.marginTop = "50px";
 
    introduce.style.fontSize = "24px";
    introduce.style.color = "#fff";
    introduce.style.cssFloat = "right";
    introduce.style.marginRight = "30px";
    introduce.style.marginTop = "100px";
}