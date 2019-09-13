openerp v5
่การตั้ง server ver 5.0 ประกอบไปด้วย 
     1 openerp-web
     2 openerp-server
     3 server.conf
     4 database
     5 path
     
คำสั่งสำหรับ run ver 5.0
    1. ./stert-web
    2. ./start-erp
    ทั้งสองข้อการรันขึ้นอยู่กับชื่อที่ตั้ง
    
สิ้งที่ต้องมีสำหรับการสร้าง Module ver 5.0 อย่างง่าย
    1. __terp__.py
    2. __init__.py
    3. file_name.py
    4. file_name_view.xml
ขั้นตอนการสร้าง
    create __terp__.py
    create __init__.py
    create file_name.py
    creat file_name_view.xml

create shotcut new module to addons by use 
    ln ../../file_name/* . # '*' เรียกทั้งหมดที่อยู่ใน Folder, '.' คือ local สำหรับ shotcut เช่น เราอยู่ใน Foder addon แล้วต้องการ shotcut 
    folder ที่ชื่อ ac_custom 
    ln ../custom-addons/ac_custom/ .
    
    
 # on the sever want create new or update database for take new module to sever
