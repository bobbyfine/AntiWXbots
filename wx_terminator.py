#coding=utf-8   //
try:
    from wxpy import *
    import daemon #Before you use Daemon please install pwd
except:
    print ("import error");
import sys
import time,platform


reload(sys)
sys.setdefaultencoding('utf-8')
#import modules
bot1 = Bot(cache_path=True); #Build robot object
gps = bot1.groups(); #get user's groups
group_list = [];
black_list = [];
chat_list = [];



def read_data():#从文档读取黑名单数据
    file = open('black_list.txt','r');
    array  = [];
    for line in file.readlines():
        line = line.strip();
        array = line.split(',');
    for word in array:
        word = word.decode('utf-8');
        if(word!=''):
            black_list.append(word);

    file.close();


read_data();

#set a default blackList





#Function dependency:  show_group_info() -> clear_bot();
def clear_bot():#清除所有群里的存在于黑名单里的bot
    count = 0;

    print(group_list);
    for group in group_list:
        if group.is_owner:
            time.sleep(5);
            remove_members_from_group(group.name);
            count = count+1;

    if(count == 0):
        print ('所有机器人已经销毁完毕! All the bots have been terminated!')

def store_data():#将黑名单写入文档
    data = open('black_list.txt','w')
    for name in black_list:
        data.write(name);
        data.write(',');
    data.close();

def show_group_info():#展示该用户所有群的信息，包括群成员
    gps = bot1.groups();
    chats = bot1.chats();
    index = 1;
    for group in gps:
        group_list.append(group);
        print('%d.%s'%(index,group.name));
        index = index + 1;
    for chat in chats:
        chat_list.append(chat);
        print (chat);



def remove_member_from_group(group_name,member_name):#清除给定群里的给定用户名的bot，并将他们保存入黑名单

    g_list = bot1.groups().search(group_name);
    g = g_list[0];

    for element in g_list:
        if element.name == group_name:
            g = element;
    for member in g:
        if member.name == member_name:
            member.remove();
            black_list.append(member.name);
            store_data();
            print("%s has been eliminated!"%member.name);



def remove_members_from_group(group_name):#清除给定群里的所有在黑名单里的bot
    try:

        g_list = bot1.groups().search(group_name);
        g = g_list[0];
        member_list = [];
        for element in g_list:
            if element.name == group_name:
                g = element;
        print(g_list);
        print(g);
        for member in g:
            if member.name in black_list :
                print (member.name);
                member_list.append(member);


        if(len(member_list)>0):
            g.remove_members(member_list);

        print('Remove success! Your Group is Clean!');


    except:
        print ('Unable to remove memebers from this group')
        return;

def monitor(): #监视器,监视bot加群行为并自动将其踢出群外
    try:
        @bot1.register(chats=chat_list)
        def print_msg(msg):
            msg_str = str(msg);
            print(msg_str);
            a1 = msg_str.split(':');
            group_name = a1[0].strip(' ');
            print(group_name);
            remove_members_from_group(group_name);





    except:
        print("Monitor error");

def redirect():
    try:
        administrator_chat = bot1.friends().search('mizushima')[0];
        c = 0;
        to_send = '';
        for g in bot1.groups():
            to_send = to_send+('%d.'%c)+str(g.name)+'\n';
            c = c + 1;
        administrator_chat.send(to_send);
        administrator_chat.send("功能1:消息转发到群，格式 group_name : message \n 功能2：一键清理群bot, 发送关键词all");
        @bot1.register(administrator_chat)
        def print_msg(msg):
                message = str(msg.text);
                print(message)
                if ':' in message:
                    temp_a = message.split(':');
                    group = bot1.groups()[int(temp_a[0])];
                    print(group);
                    group.send(temp_a[1]);
                elif message == 'all':
                    show_group_info();
                    clear_bot();

    except:
        print("Redirect error");


def main_loop():
    while 1:


        show_group_info();


        input = raw_input('Deletemode:\t1.删除指定群里的黑名单bot \t 2.删除指定群里的指定用户并将其加入黑名单 \t q.退出程序 \t all.核弹选项(nuclear optionn)，删除所有群里的所有bot\n')

        if(input=='q'):
            break;
        elif input == 'all'.upper() or input == 'all':
            clear_bot();
        elif input =='1':
            groupInput = raw_input("输入群名,见列表");
            remove_members_from_group(groupInput);
        elif input =='2':
            groupInput = raw_input("输入群名，见列表");
            botName = raw_input("输入bot用户名，见列表");
            remove_member_from_group(groupInput,botName);
        elif input == 'ls':
            show_group_info();






def auto_monitoring():
    while 1:
        show_group_info();
        clear_bot();
        monitor();
        time.sleep(7200);  ##每2个小时(7200sec)自动清理一次机器人

def redirect_msg():
    redirect();
    bot1.join();


def with_daemon():
    with daemon.DaemonContext():
        main_loop();


if __name__ == '__main__':
    if(platform.system()=='Linux'):
        with_daemon();
    else:
        main_loop();
        #redirect_msg();
        #auto_monitoring();