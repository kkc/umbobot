# -*- coding: utf8 -*-
"""
errbot plugin - ChitChat
"""
import urllib
import json
import random
import threading
import time
import datetime
from time import strftime
from subprocess import call
import pymongo
import bson
from pymongo import MongoClient
from pymongo import CursorType
import time

import re
import sys
from errbot import BotPlugin, botcmd
import requests
from get_action import getAction
#from get_reminder import getReminder, key_WeekOfDay, key_Hour, key_min, key_msg, key_chance


reload(sys)
sys.setdefaultencoding("utf-8")

# how many lines of dialog will umbobot remember
MaxHistory = 50

# how many lines of dialog will umbobot consider it as message to umbobot itself
MaxComprehensiveLine = 4

LastUpdateTime = 0

emoji = [':bowtie:', ':smile:', ':laughing:', ':blush:', ':smiley:', ':relaxed:', ':smirk:', ':heart_eyes:', ':kissing_heart:',
         ':kissing_closed_eyes:', ':flushed:', ':relieved:', ':satisfied:', ':grin:', ':wink:', ':stuck_out_tongue_winking_eye:',
         ':stuck_out_tongue_closed_eyes:', ':grinning:', ':kissing:', ':kissing_smiling_eyes:', ':stuck_out_tongue:', ':sleeping:',
         ':worried:', ':frowning:', ':anguished:', ':open_mouth:', ':grimacing:', ':confused:', ':hushed:', ':expressionless:',
         ':unamused:', ':sweat_smile:', ':sweat:', ':disappointed_relieved:', ':weary:', ':pensive:', ':disappointed:', ':confounded:',
         ':fearful:', ':cold_sweat:', ':persevere:', ':cry:', ':sob:', ':joy:', ':astonished:', ':scream:', ':neckbeard:',
         ':tired_face:', ':angry:', ':rage:', ':triumph:', ':sleepy:', ':yum:', ':mask:', ':sunglasses:', ':dizzy_face:', ':imp:',
         ':smiling_imp:', ':neutral_face:', ':no_mouth:', ':innocent:', ':alien:', ':yellow_heart:', ':blue_heart:', ':purple_heart:',
         ':heart:', ':green_heart:', ':broken_heart:', ':heartbeat:', ':heartpulse:', ':two_hearts:', ':revolving_hearts:', ':cupid:',
         ':sparkling_heart:', ':sparkles:', ':star:', ':star2:', ':dizzy:', ':boom:', ':collision:', ':anger:', ':exclamation:',
         ':question:', ':grey_exclamation:', ':grey_question:', ':zzz:', ':dash:', ':sweat_drops:', ':notes:', ':musical_note:',
         ':fire:', ':hankey:', ':poop:', ':shit:', ':+1:', ':thumbsup:', ':-1:', ':thumbsdown:', ':ok_hand:', ':punch:', ':facepunch:',
         ':fist:', ':v:', ':wave:', ':hand:', ':raised_hand:', ':open_hands:', ':point_up:', ':point_down:', ':point_left:',
         ':point_right:', ':raised_hands:', ':pray:', ':point_up_2:', ':clap:', ':muscle:', ':metal:', ':fu:', ':walking:', ':runner:',
         ':running:', ':couple:', ':family:', ':two_men_holding_hands:', ':two_women_holding_hands:', ':dancer:', ':dancers:',
         ':ok_woman:', ':no_good:', ':information_desk_person:', ':raising_hand:', ':bride_with_veil:', ':person_with_pouting_face:',
         ':person_frowning:', ':bow:', ':couplekiss:', ':couple_with_heart:', ':massage:', ':haircut:', ':nail_care:', ':boy:',
         ':girl:', ':woman:', ':man:', ':baby:', ':older_woman:', ':older_man:', ':person_with_blond_hair:', ':man_with_gua_pi_mao:',
         ':man_with_turban:', ':construction_worker:', ':cop:', ':angel:', ':princess:', ':smiley_cat:', ':smile_cat:',
         ':heart_eyes_cat:', ':kissing_cat:', ':smirk_cat:', ':scream_cat:', ':crying_cat_face:', ':joy_cat:', ':pouting_cat:',
         ':japanese_ogre:', ':japanese_goblin:', ':see_no_evil:', ':hear_no_evil:', ':speak_no_evil:', ':guardsman:', ':skull:',
         ':feet:', ':lips:', ':kiss:', ':droplet:', ':ear:', ':eyes:', ':nose:', ':tongue:', ':love_letter:', ':bust_in_silhouette:',
         ':busts_in_silhouette:', ':speech_balloon:', ':thought_balloon:', ':feelsgood:', ':finnadie:', ':goberserk:', ':godmode:',
         ':hurtrealbad:', ':rage1:', ':rage2:', ':rage3:', ':rage4:', ':suspect:', ':trollface:', ':sunny:', ':umbrella:', ':cloud:',
         ':snowflake:', ':snowman:', ':zap:', ':cyclone:', ':foggy:', ':ocean:', ':cat:', ':dog:', ':mouse:', ':hamster:', ':rabbit:',
         ':wolf:', ':frog:', ':tiger:', ':koala:', ':bear:', ':pig:', ':pig_nose:', ':cow:', ':boar:', ':monkey_face:', ':monkey:',
         ':horse:', ':racehorse:', ':camel:', ':sheep:', ':elephant:', ':panda_face:', ':snake:', ':bird:', ':baby_chick:',
         ':hatched_chick:', ':hatching_chick:', ':chicken:', ':penguin:', ':turtle:', ':bug:', ':honeybee:', ':ant:', ':beetle:',
         ':snail:', ':octopus:', ':tropical_fish:', ':fish:', ':whale:', ':whale2:', ':dolphin:', ':cow2:', ':ram:', ':rat:',
         ':water_buffalo:', ':tiger2:', ':rabbit2:', ':dragon:', ':goat:', ':rooster:', ':dog2:', ':pig2:', ':mouse2:', ':ox:',
         ':dragon_face:', ':blowfish:', ':crocodile:', ':dromedary_camel:', ':leopard:', ':cat2:', ':poodle:', ':paw_prints:',
         ':bouquet:', ':cherry_blossom:', ':tulip:', ':four_leaf_clover:', ':rose:', ':sunflower:', ':hibiscus:', ':maple_leaf:',
         ':leaves:', ':fallen_leaf:', ':herb:', ':mushroom:', ':cactus:', ':palm_tree:', ':evergreen_tree:', ':deciduous_tree:',
         ':chestnut:', ':seedling:', ':blossom:', ':ear_of_rice:', ':shell:', ':globe_with_meridians:', ':sun_with_face:',
         ':full_moon_with_face:', ':new_moon_with_face:', ':new_moon:', ':waxing_crescent_moon:', ':first_quarter_moon:',
         ':waxing_gibbous_moon:', ':full_moon:', ':waning_gibbous_moon:', ':last_quarter_moon:', ':waning_crescent_moon:',
         ':last_quarter_moon_with_face:', ':first_quarter_moon_with_face:', ':moon:', ':earth_africa:', ':earth_americas:',
         ':earth_asia:', ':volcano:', ':milky_way:', ':partly_sunny:', ':octocat:', ':squirrel:', ':bamboo:', ':gift_heart:',
         ':dolls:', ':school_satchel:', ':mortar_board:', ':flags:', ':fireworks:', ':sparkler:', ':wind_chime:', ':rice_scene:',
         ':jack_o_lantern:', ':ghost:', ':santa:', ':christmas_tree:', ':gift:', ':bell:', ':no_bell:', ':tanabata_tree:', ':tada:',
         ':confetti_ball:', ':balloon:', ':crystal_ball:', ':cd:', ':dvd:', ':floppy_disk:', ':camera:', ':video_camera:',
         ':movie_camera:', ':computer:', ':tv:', ':iphone:', ':phone:', ':telephone:', ':telephone_receiver:', ':pager:', ':fax:',
         ':minidisc:', ':vhs:', ':sound:', ':speaker:', ':mute:', ':loudspeaker:', ':mega:', ':hourglass:', ':hourglass_flowing_sand:',
         ':alarm_clock:', ':watch:', ':radio:', ':satellite:', ':loop:', ':mag:', ':mag_right:', ':unlock:', ':lock:',
         ':lock_with_ink_pen:', ':closed_lock_with_key:', ':key:', ':bulb:', ':flashlight:', ':high_brightness:', ':low_brightness:',
         ':electric_plug:', ':battery:', ':calling:', ':email:', ':mailbox:', ':postbox:', ':bath:', ':bathtub:', ':shower:',
         ':toilet:', ':wrench:', ':nut_and_bolt:', ':hammer:', ':seat:', ':moneybag:', ':yen:', ':dollar:', ':pound:', ':euro:',
         ':credit_card:', ':money_with_wings:', ':e-mail:', ':inbox_tray:', ':outbox_tray:', ':envelope:', ':incoming_envelope:',
         ':postal_horn:', ':mailbox_closed:', ':mailbox_with_mail:', ':mailbox_with_no_mail:', ':package:', ':door:', ':smoking:',
         ':bomb:', ':gun:', ':hocho:', ':pill:', ':syringe:', ':page_facing_up:', ':page_with_curl:', ':bookmark_tabs:', ':bar_chart:',
         ':chart_with_upwards_trend:', ':chart_with_downwards_trend:', ':scroll:', ':clipboard:', ':calendar:', ':date:',
         ':card_index:', ':file_folder:', ':open_file_folder:', ':scissors:', ':pushpin:', ':paperclip:', ':black_nib:', ':pencil2:',
         ':straight_ruler:', ':triangular_ruler:', ':closed_book:', ':green_book:', ':blue_book:', ':orange_book:', ':notebook:',
         ':notebook_with_decorative_cover:', ':ledger:', ':books:', ':bookmark:', ':name_badge:', ':microscope:', ':telescope:',
         ':newspaper:', ':football:', ':basketball:', ':soccer:', ':baseball:', ':tennis:', ':8ball:', ':rugby_football:', ':bowling:',
         ':golf:', ':mountain_bicyclist:', ':bicyclist:', ':horse_racing:', ':snowboarder:', ':swimmer:', ':surfer:', ':ski:',
         ':spades:', ':hearts:', ':clubs:', ':diamonds:', ':gem:', ':ring:', ':trophy:', ':musical_score:', ':musical_keyboard:',
         ':violin:', ':space_invader:', ':video_game:', ':black_joker:', ':flower_playing_cards:', ':game_die:', ':dart:', ':mahjong:',
         ':clapper:', ':memo:', ':pencil:', ':book:', ':art:', ':microphone:', ':headphones:', ':trumpet:', ':saxophone:', ':guitar:',
         ':shoe:', ':sandal:', ':high_heel:', ':lipstick:', ':boot:', ':shirt:', ':tshirt:', ':necktie:', ':womans_clothes:',
         ':dress:', ':running_shirt_with_sash:', ':jeans:', ':kimono:', ':bikini:', ':ribbon:', ':tophat:', ':crown:', ':womans_hat:',
         ':mans_shoe:', ':closed_umbrella:', ':briefcase:', ':handbag:', ':pouch:', ':purse:', ':eyeglasses:',
         ':fishing_pole_and_fish:', ':coffee:', ':tea:', ':sake:', ':baby_bottle:', ':beer:', ':beers:', ':cocktail:',
         ':tropical_drink:', ':wine_glass:', ':fork_and_knife:', ':pizza:', ':hamburger:', ':fries:', ':poultry_leg:',
         ':meat_on_bone:', ':spaghetti:', ':curry:', ':fried_shrimp:', ':bento:', ':sushi:', ':fish_cake:', ':rice_ball:',
         ':rice_cracker:', ':rice:', ':ramen:', ':stew:', ':oden:', ':dango:', ':egg:', ':bread:', ':doughnut:', ':custard:',
         ':icecream:', ':ice_cream:', ':shaved_ice:', ':birthday:', ':cake:', ':cookie:', ':chocolate_bar:', ':candy:', ':lollipop:',
         ':honey_pot:', ':apple:', ':green_apple:', ':tangerine:', ':lemon:', ':cherries:', ':grapes:', ':watermelon:', ':strawberry:',
         ':peach:', ':melon:', ':banana:', ':pear:', ':pineapple:', ':sweet_potato:', ':eggplant:', ':tomato:', ':corn:', 'Places', '',
         ':house:', ':house_with_garden:', ':school:', ':office:', ':post_office:', ':hospital:', ':bank:', ':convenience_store:',
         ':love_hotel:', ':hotel:', ':wedding:', ':church:', ':department_store:', ':european_post_office:', ':city_sunrise:',
         ':city_sunset:', ':japanese_castle:', ':european_castle:', ':tent:', ':factory:', ':tokyo_tower:', ':japan:', ':mount_fuji:',
         ':sunrise_over_mountains:', ':sunrise:', ':stars:', ':statue_of_liberty:', ':bridge_at_night:', ':carousel_horse:',
         ':rainbow:', ':ferris_wheel:', ':fountain:', ':roller_coaster:', ':ship:', ':speedboat:', ':boat:', ':sailboat:', ':rowboat:',
         ':anchor:', ':rocket:', ':airplane:', ':helicopter:', ':steam_locomotive:', ':tram:', ':mountain_railway:', ':bike:',
         ':aerial_tramway:', ':suspension_railway:', ':mountain_cableway:', ':tractor:', ':blue_car:', ':oncoming_automobile:',
         ':car:', ':red_car:', ':taxi:', ':oncoming_taxi:', ':articulated_lorry:', ':bus:', ':oncoming_bus:', ':rotating_light:',
         ':police_car:', ':oncoming_police_car:', ':fire_engine:', ':ambulance:', ':minibus:', ':truck:', ':train:', ':station:',
         ':train2:', ':bullettrain_front:', ':bullettrain_side:', ':light_rail:', ':monorail:', ':railway_car:', ':trolleybus:',
         ':ticket:', ':fuelpump:', ':vertical_traffic_light:', ':traffic_light:', ':warning:', ':construction:', ':beginner:', ':atm:',
         ':slot_machine:', ':busstop:', ':barber:', ':hotsprings:', ':checkered_flag:', ':crossed_flags:', ':izakaya_lantern:',
         ':moyai:', ':circus_tent:', ':performing_arts:', ':round_pushpin:', ':triangular_flag_on_post:', ':jp:', ':kr:', ':cn:',
         ':us:', ':fr:', ':es:', ':it:', ':ru:', ':gb:', ':uk:', ':de:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:',
         ':seven:', ':eight:', ':nine:', ':keycap_ten:', ':1234:', ':zero:', ':hash:', ':symbols:', ':arrow_backward:', ':arrow_down:',
         ':arrow_forward:', ':arrow_left:', ':capital_abcd:', ':abcd:', ':abc:', ':arrow_lower_left:', ':arrow_lower_right:',
         ':arrow_right:', ':arrow_up:', ':arrow_upper_left:', ':arrow_upper_right:', ':arrow_double_down:', ':arrow_double_up:',
         ':arrow_down_small:', ':arrow_heading_down:', ':arrow_heading_up:', ':leftwards_arrow_with_hook:', ':arrow_right_hook:',
         ':left_right_arrow:', ':arrow_up_down:', ':arrow_up_small:', ':arrows_clockwise:', ':arrows_counterclockwise:', ':rewind:',
         ':fast_forward:', ':information_source:', ':ok:', ':twisted_rightwards_arrows:', ':repeat:', ':repeat_one:', ':new:', ':top:',
         ':up:', ':cool:', ':free:', ':ng:', ':cinema:', ':koko:', ':signal_strength:', ':u5272:', ':u5408:', ':u55b6:', ':u6307:',
         ':u6708:', ':u6709:', ':u6e80:', ':u7121:', ':u7533:', ':u7a7a:', ':u7981:', ':sa:', ':restroom:', ':mens:', ':womens:',
         ':baby_symbol:', ':no_smoking:', ':parking:', ':wheelchair:', ':metro:', ':baggage_claim:', ':accept:', ':wc:',
         ':potable_water:', ':put_litter_in_its_place:', ':secret:', ':congratulations:', ':m:', ':passport_control:',
         ':left_luggage:', ':customs:', ':ideograph_advantage:', ':cl:', ':sos:', ':id:', ':no_entry_sign:', ':underage:',
         ':no_mobile_phones:', ':do_not_litter:', ':non-potable_water:', ':no_bicycles:', ':no_pedestrians:', ':children_crossing:',
         ':no_entry:', ':eight_spoked_asterisk:', ':sparkle:', ':eight_pointed_black_star:', ':heart_decoration:', ':vs:',
         ':vibration_mode:', ':mobile_phone_off:', ':chart:', ':currency_exchange:', ':negative_squared_cross_mark:', ':a:', ':b:',
         ':ab:', ':o2:', ':diamond_shape_with_a_dot_inside:', ':recycle:', ':end:', ':back:', ':on:', ':soon:', ':clock1:',
         ':clock130:', ':clock10:', ':clock1030:', ':clock11:', ':clock1130:', ':clock12:', ':clock1230:', ':clock2:', ':clock230:',
         ':clock3:', ':clock330:', ':clock4:', ':clock430:', ':clock5:', ':clock530:', ':clock6:', ':clock630:', ':clock7:',
         ':clock730:', ':clock8:', ':clock830:', ':clock9:', ':clock930:', ':heavy_dollar_sign:', ':copyright:', ':registered:',
         ':tm:', ':x:', ':heavy_exclamation_mark:', ':bangbang:', ':interrobang:', ':o:', ':heavy_multiplication_x:',
         ':heavy_plus_sign:', ':heavy_minus_sign:', ':heavy_division_sign:', ':white_flower:', ':100:', ':heavy_check_mark:',
         ':ballot_box_with_check:', ':radio_button:', ':link:', ':curly_loop:', ':wavy_dash:', ':part_alternation_mark:', ':trident:',
         ':black_small_square:', ':white_small_square:', ':black_medium_small_square:', ':white_medium_small_square:',
         ':black_medium_square:', ':white_medium_square:', ':black_large_square:', ':white_large_square:', ':white_check_mark:',
         ':black_square_button:', ':white_square_button:', ':black_circle:', ':white_circle:', ':red_circle:', ':large_blue_circle:',
         ':large_blue_diamond:', ':large_orange_diamond:', ':small_blue_diamond:', ':small_orange_diamond:', ':small_red_triangle:',
         ':small_red_triangle_down:', ':shipit:', ':godmode:']

happyString = ['爽', '好笑', '笑死']
sadString = ['受傷', '難過', '生病', '請假', 'Q_Q', 'QQ']
angryString = ['umbobot*爛']

mMessage = -1
mMessageTime = 0

mReminder = ''

speaker = ''
speak_out = False

lsat_idx = 0




# time gap in sec, if you changed this value, plz change TimerThread gap 'if' constrain accordingly
# default value: 300
timeGap = 300
DEFAULT_POLL_INTERVAL = 60 # One minutes


def zhprint(obj):
    import re

    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


def checkTime(hour, min):
    mHour = datetime.datetime.now().hour
    mMinute = datetime.datetime.now().minute

    if mHour >= int(hour) and mHour < int(hour) + 1 and mMinute >= int(min) and mMinute < int(min) + (timeGap / 60):
        return True
    else:
        return False


def checkDay(days_of_week):
    day_list = list(days_of_week)
    for d in day_list:
        if datetime.datetime.today().weekday() == int(d):
            return True
    return False


class Chitchatt(BotPlugin):
    ''' Annoying chit chat plugin
    '''
    #min_err_version = '1.6.0'  # Optional, but recommended
    #max_err_version = '3.4.0'  # Optional, but recommended
    decayValue = 20
    girl_source = ''

    histMsg = []
    histFrom = []
    histFromNick = []
    histChecked = []
    histPisiton = 0

    happy = 0
    sad = 0
    angry = 0
    lastCheckTime = 0
    lastLunchTime = 0
    lastDinnerTime = 0

    isCheckThreadStarted = False


    # log control
    ShowCompareLog = True
    ShowEmoLog = False
    ShowTalkHis = True
    ShowAntiWash = True
    show_reminder_log = True

    UpdateActionInterval = 3600
    LastUpdateTime = 0

    action_list = []

    hatedPeopleName = ''
    likePeopleName = ''

    noteList = []

    # imform edward
    client = None
    customerData_coll = None
    last_record = None
    record_file_handler = None

    # mSelf =''

    @botcmd
    def chitchatt(self, msg, args):
        """Say hello to someone"""
        return "Hello, " + format(msg.frm)

    def send_customer_data(self):
        cursor = self.customerData_coll.find({'_id': {'$gt': bson.objectid.ObjectId(self.last_record)}}, cursor_type = CursorType.TAILABLE_AWAIT)
	try:
            while cursor.alive:
                try:
                    doc = cursor.next()
		    if doc is not None:
   	                self.last_record = doc['_id']
		    message = random.choice(["@edwardchen 哥, 你的快遞來了\n", "好像有什麼不得了的東西\n", "@edwardchen: 鐺鐺鐺鐺\n",
					     "來了來了\n", "被洗版了\n"])
		    time.sleep(5)
	            if 'comment' in doc:
	                message += "```email:%s, comment:%s, date:%s```" % (doc['email'], doc['comment'], doc['_id'].generation_time)
		    else:
			message += "```company:%s, name:%s, countryCode:%s, phone:%s, type:%s, email:%s, date:%s```" % (doc['company'], doc['firstName'] + doc['lastName'], doc['countryCode'], doc['phone'], doc['type'], doc['email'], doc['_id'].generation_time)
                    self.send(self.build_identifier('#bot'), message)
                    print doc
                except StopIteration:
		    if self.last_record:
			self.record_file_handler = open('last_record', 'w')
		        self.record_file_handler.write(str(self.last_record))
			self.record_file_handler.close()
                    break
	except pymongo.errors.OperationFailure:
            print "Delete the collection while running to see this."
        except KeyboardInterrupt:
            print "Ctrl-C Ya!"
            sys.exit(0)

    def test(self):
        self.log.debug("test polling every sec")


    def deactivate(self):
        super(Chitchat, self).deactivate()

    def send_from_messages(self, message_list):
        msg_count = 0

        for msg in message_list:

            msg_len = len(msg)
            if msg_len < 5:
                msg_len = 5

            sleep_time = random.uniform(0, 0.3) * msg_len
            if(msg.startswith('http')):
                sleep_time = 1
            elif sleep_time > 9:
                sleep_time = 7 + random.uniform(0, 2)

            # speaking act as sleeping time already, no need to add extra sleep time
            if not speak_out or msg_count == 0:
                time.sleep(sleep_time)

            msg = msg.replace('randname', '@' + str(random.choice(self.histFromNick)))
            msg = msg.replace('randmsg', random.choice(self.histMsg))
            msg = msg.replace('@umbobot', "我")

            self.send(mMessage.to, msg, message_type=mMessage.type)

            if self.ShowCompareLog:
                zhprint(' **message "' + msg + '" sended')

            msg_count += 1

            idx = lsat_idx
            while idx < len(self.histMsg):
                self.histChecked[idx] = True
                idx += 1

            # check speaker
            if speak_out and not msg.startswith('http'):
                global speaker

                # detect language
                detected_string_kr1 = re.findall(ur'[\u1100-\u11ff]+', msg)
                detected_string_kr2 = re.findall(ur'[\uac00-\ud7af]+', msg)
                detected_string_jp = re.findall(ur'[\u3040-\u30ff]+', msg)

                if len(speaker) > 0:
                    call(["say", "-v", speaker, msg])
                    print 'speak as custom speaker: ', speaker
                    # reset speaker
                    speaker = ''

                elif len(detected_string_jp) > 0:
                    call(["say", "-v", 'kyoko', msg])
                    print 'speak as japanese'

                elif len(detected_string_kr1) > 0 or len(detected_string_kr2) > 0:
                    call(["say", "-v", 'yuna', msg])
                    print 'speak as korean'

                else:
                    call(["say", msg])
                    print 'speak as default speaker'

    # this thread check schedule and response
    class TimerThread(threading.Thread):

        mChitChat = ''

        def __init__(self, chitchat_self):
            print '** checking thread started **'
            threading.Thread.__init__(self)

            self.mChitChat = chitchat_self

            print 'timer thread started!'


        def run(self):
            while (True):
                print '** check reminder: ', strftime("%Y-%m-%d %H:%M:%S", ), ' **'

                # weather forecast
                if ( checkTime(9, 10) or checkTime(12, 30) or checkTime(19, 10)) and \
                        checkDay('01234') and random.randrange(0, 101) > 98:
                    print 'show weather forecast reminder'
                    self.mChitChat.showWeahterForcast()

                # meetup reminder
                # TODO

                # auto talkonButtonClickListener
                if (int(time.time()) - mMessageTime) > 3600 * 20 and datetime.datetime.now().hour > 10 and datetime.datetime.now().hour < 20 and random.randrange(0, 101) < 3 and checkDay('01234'):
                    askMsg = ['吃飯啊', '走了 吃飯啊', '有人要吃東西嗎', '吃飯吃飯吃飯吃飯吃飯', '都沒有人要跟我完', '有人在嗎？？', '幫我開門', '肚子餓了', '大家還在嗎？',
                    '怎麼這麼久都沒有人留言？', '大家好，我是umbobot', '都沒人留言 大家都放假去了嗎？', '今天天氣不錯']
                    self.mChitChat.send_from_messages(random.choice(askMsg))

                    # global mMessageTime
                    mMessageTime = int(time.time())


                # load reminder from spreadsheet
                #reminder = getReminder()
                #for r in reminder:
                #    match_day = checkDay(r[key_WeekOfDay])
                #    match_time = checkTime(r[key_Hour], r[key_min])

                #    if self.mChitChat.show_reminder_log:
                #        check_status = ''
                #        if match_day:
                #            check_status += '  day matched(' + r[key_WeekOfDay] + ')   '
                #        else:
                #            check_status += '  day not matched(' + r[key_WeekOfDay] + ')   '

                #        if match_time:
                #            check_status += 'time matched(' + r[key_Hour] + ':' + r[key_min] + ')'
                #        else:
                #            check_status += 'time not matched(' + r[key_Hour] + ':' + r[key_min] + ')'

                #        zhprint('reminder check: ' + r[key_msg][0] + check_status)

                #    if match_day and match_time:
                #        print '**time matched**'

                #        if random.randrange(0, 101) < int(r[key_chance]):
                #            print 'roll < ' + r[key_chance] + ', success!'
                #            self.mChitChat.send_from_messages(random.choice(r[key_msg]).split('*'))

                #        else:
                #            print 'roll > ' + r[key_chance] + ', failed!'


                # setting status is not working on umbobot??

                # if random.randrange(0, 101) < 100:
                # print '** change status **'
                # selfStatus = ['/available 希望的種子', '/available 我不是網軍', '/available 心情不好 QQ', '/available 期待你來給我安慰',
                # '/available 驚奇4曹仁', '/available 驚奇4曹仁', '/available 驚奇4曹仁', '/available 魏延既出，司馬難追 ',
                # '/available 司馬當活馬醫', '/available 乳搖知馬力-日久變人妻', '/available 你真的很閒 沒事看我的狀態']
                #
                # if mMessage != -1:
                #
                # print self.mChitChat
                # print mMessage
                #
                # self.mChitChat.send(mMessage.getFrom(), random.choice(selfStatus), message_type=mMessage.getType())
                # print 'changed status'

                time.sleep(timeGap)


    def loadCurrentNote(self):
        file = open('user/Document/umbobot/umbobot.sav', 'w+')


    def saveCurrentNote(self):
        file = open('user/Document/umbobot/umbobot.sav', 'w+')
        jsonFile = json.load(file)


    def checkUpdateKeyword(self):
        currentTime = int(time.time())

        difference = (currentTime - self.LastUpdateTime )

        if difference > self.UpdateActionInterval:
            print 'last update more than a hour, re-fetch from spreadsheet: ', difference
            self.action_list = getAction()
            print 'action updated, total ', len(self.action_list), 'action now'
            self.LastUpdateTime = currentTime
            print 'action LastUpdateTime ', self.LastUpdateTime


    def saveHist(self, message, Msgfrom):

        self.histMsg.append(message)
        self.histFrom.append(Msgfrom)
        self.histFromNick.append(Msgfrom.nick)
        self.histChecked.append(False)

        if len(self.histMsg) > MaxHistory:
            self.histMsg.pop(0)
            self.histFrom.pop(0)
            self.histFromNick.pop(0)
            self.histChecked.pop(0)

        if self.ShowTalkHis:
            print '**** printing hist msg ****'
            histMsg = []

            for msg in self.histMsg:
                histMsg.append(msg)
            i = 0
            for name in self.histFromNick:
                histMsg[i] = str(name) + ' said:  ' + str(histMsg[i]) + '   status: ' + str(self.histChecked[i])
                i += 1

            for msg in histMsg:
                zhprint(msg)

            print '**** end of hist ****'

    def findLongestSubstring(self, source,target):
        m = len(source)
        n = len(target)
        counter = [[0]*(n+1) for x in range(m+1)]
        longest = 0
        lcs_set = set()
        for i in range(m):
            for j in range(n):
                if source[i].lower() == target[j].lower():
                    c = counter[i][j] + 1
                    counter[i+1][j+1] = c
                    if c > longest:
                        lcs_set = set()
                        longest = c
                        lcs_set.add(source[i-c+1:i+1])
                    elif c == longest:
                        lcs_set.add(source[i-c+1:i+1])
        result = ""
        for item in lcs_set:
            result = result + item
        return result

    def extractKeyword(self, message_string):
        param_q = message_string.replace('umbobot', '').replace('@', '').replace(': ', '');
        param_q = param_q.replace('你', '').replace('妳', '').replace('我', '').replace('他', '').replace('她', '').replace('它', '').replace('祂', '')
        param_q = param_q.replace('請問', '')
        param_q = param_q.replace('可不可以', '').replace('會不會', '').replace('能不能', '').replace('是不是', '')
        param_q = param_q.replace('知不知道', '').replace('了不了解', '').replace('瞭不瞭解', '').replace('曉不曉得', '').replace('熟不熟悉', '').replace('懂不懂', '')
        param_q = param_q.replace('可以', '').replace('會', '').replace('能', '').replace('是', '')
        param_q = param_q.replace('知道', '').replace('了解', '').replace('瞭解', '').replace('曉得', '').replace('熟悉', '').replace('懂', '')
        param_q = param_q.replace('了', '').replace('吧', '').replace('呢', '').replace('嗎', '')
        param_q = param_q.replace('?', '').replace('!', '')

        if len(param_q) <= 4:
            return param_q

        # TODO: need to implement sentence sengmentation

        return param_q

    def replySearchResultFail(self):
        preReplyArray = ['我找不到，我找不到', '我不會，我不會', '這就是我的極限啊', '我也不知道']
        postReplyArray = ['(掩面)', '(已哭)', '，為什麼要逼我!?', '(已難過)', ' :weary: ']
        catReply = random.choice(preReplyArray) + random.choice(postReplyArray)
        self.send_from_messages([catReply])

    def searchResult(self, message_string, ask_umbobot):
        print '**** try to google it ****'
        print 'message:' + message_string

        randomNum = random.random()

        if not ask_umbobot and randomNum <= 0.8:
            print '**** send search result FAIL: not for umbobot and random number is less 0.8 ****'
            return False

        if ask_umbobot and ('你' in message_string) and ('怎麼' in message_string) and ('在' in message_string):
            self.send_from_messages(['嚴格來說，我也是開發者啊'])
            return True

        domain = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyBZplnKkoxdXglif9Qq1eKTGUs9_fIT0j8&cx=015657725914316056186:2vam3hjyk5u&'
        param_q = self.extractKeyword(message_string)

        if len(param_q) == 0:
            print '**** send search result FAIL: cannot find keyword ****'
            return False

        if not '請問' in message_string:
            if ask_umbobot and random.random() <= 0.4: # 中斷掉 search function
                replyArray = ['很可怕，不要問', '我也不是隨隨便便教人的，先走了，掰', '叫我出聲我就出聲，那豈不是很沒面子，先洗澡了，掰', '你自己來?我媽叫我吃飯了，掰', '想問我的話要加請問', '小朋友，問人問題要加請問喔!', '需要我幫忙的話就加請問喔，不要害羞']
                reply = random.choice(replyArray)
                print '**** send interrupted reply: ' + reply + ' ****'
                self.send_from_messages([reply])
                return True

        q = { 'q' : param_q, 'safe': 'medium' }
        print '**** search result url: ' + domain + urllib.urlencode(q) + ' ****'
        responseData = json.loads(requests.get(domain + urllib.urlencode(q)).content)

        if not responseData or 'items' not in responseData:
            print '**** send search result FAIL: responseData == null ****'
            self.replySearchResultFail()
            return True

        length = len(responseData['items'])

        if length == 0:
            print '**** send search result FAIL: length == 0 ****'
            self.replySearchResultFail()
            return True

        if not responseData:
            print '**** send search result FAIL: responseData == null ****'
            self.replySearchResultFail()
            return True

        index = int(random.random() * length)
        result = responseData['items'][index]['link']
        if result:
            print '**** check search result: ' + result + ' ****'
            checkAvailable = urllib.urlopen(result)
            if checkAvailable.getcode() == 404:
                print '**** check search result FAIL: result is 404 ****'
                self.replySearchResultFail()
                return True

            if ask_umbobot:
                if '會' in message_string or '知道' in message_string or '曉得' in message_string or '了解' in message_string or '瞭解' in message_string or '熟悉' in message_string or '懂' in message_string:
                    replyArray = ['這還用問嗎?', '我是精英耶！', 'Of Course~', '你哪位?', '問這麼沒水準的問題']
                    reply = random.choice(replyArray) + ' ' + random.choice(replyArray)
                    self.send_from_messages([reply])

                preReplyArray = ['經過我媲美 google 的龐大資料庫搜尋後', '看在你誠心誠意的份上', '我也不是隨便的人', '經過我的工人智慧判斷', '我想想看', '我猜猜看', '我問一下google', '我擲一下茭', '我冥想了一下']
                postReplyArray = ['...好吧', '，就賞你一個...', '，一定就是這個了', '，是這個嗎?', '，有對嗎?', '，真相只有一個!', '，我只告訴你喔', '，原本不想說的']
                catReply = random.choice(preReplyArray) + random.choice(postReplyArray)
                self.send_from_messages([catReply])

            print '**** send search result: ' + result + ' ****'
            self.send_from_messages([result])
            return True
        else:
            print '**** send search result FAIL: result == null ****'
            self.replySearchResultFail()
            return True

    # check if previous talk contain keyword
    def prevContain(self, keywordArray):
        for key in keywordArray:
            for prevMsg in self.histMsg:
                if key in prevMsg:
                    return True
        return False


    def checkWeather(self, message_string):
        if random.randrange(0, 11) < 2:
            return False
        else:

            if self.checkIfContain([u'天氣', u'氣溫']):
                # otherDes = [u'早上', u'晚上', u'飯', u'上班', u'餐', u'下班', u'出門']
                #
                # print 'check weather roll success, keyword matched'
                # if self.prevContain(otherDes) or self.checkIfContain(otherDes, message_string):
                # self.showWeahterForcast()
                # else:

                place = 'taipei'
                if self.checkIfContain([u'倫敦']):
                    place = 'london'

                self.showWeahterForcast(place)

                return True
            return False


    def showWeahterNow(self):
        weather = json.loads(
            requests.get('http://api.openweathermap.org/data/2.5/weather?q=taipei&lang=zh_tw').content)

        prefixArray = ['感謝@Vin大大，現在的天氣是', 'hihi~  現在的天氣是', '現在外面天氣是', '外面天氣', '現在外面天氣是', '外面天氣'
                                                                                         '因為' + random.choice(
            self.histFromNick) + '的關係，現在的天氣是']
        midfixArray = [' 氣溫是', ',溫度有', '，結果氣溫', '，然後氣溫是']
        subfixArray = [
            '度', '度', '度', '度，真的不是人在待的', '度, 可去外面曬曬太陽', '度, 意圖令人開冷氣', '度, 我都快熱當了!!', '有夠冷', '令人打了個韓戰', '記得多加件外套',
            '度，外出多加注意歐', '度，不要忘了防曬歐', '度，真是冷死人了', '度，不是很適合出門', '，真想待在家裡不出門....', '', '', '']
        msg = random.choice(prefixArray) + weather['weather'][0]['description'] + random.choice(
            midfixArray) + str((int(weather['main']['temp']) - 273.15)) + random.choice(subfixArray)
        self.send(mMessage.getFrom(), msg,
                  message_type=mMessage.getType())

        if u"雨" in weather['weather'][0]['description'] or u"多雲" in weather['weather'][0]['description'] \
                or u"晴" in weather['weather'][0]['description'] and (int(weather['main']['temp']) - 273.15) > 30:
            rainNoti = ['記得提醒@vin大大帶傘', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘',
                        '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！']
            self.send(mMessage.getFrom(), random.choice(rainNoti), message_type=mMessage.getType())


    def showWeahterForcast(self, place):
        weatherToday = json.loads(
            requests.get('http://api.openweathermap.org/data/2.5/forecast?q=' + place + '&lang=zh_tw&appid=25ea212e2e5f81ce20695e089e772169').content)

        currentTime = int(time.strftime("%H"))
        forcastTimeZone = 0

        if currentTime < 4:
            prefixArray = ['明天上班天氣是', '明天早上上班天氣是', 'hihi 明天早上上班天氣是']
            forcastTimeZone = 0
        elif currentTime < 10:
            prefixArray = ['今天上班天氣是', '上班外面天氣是']
            forcastTimeZone = 0
        elif currentTime < 13:
            prefixArray = [
                '中午吃飯天氣是', '中午外面天氣', '中午吃飯天氣是', '中午外面天氣', '感謝@vin大大，今天中午吃飯的天氣是']
            forcastTimeZone = 1
        elif currentTime < 17:
            prefixArray = ['今天下班天氣是', 'hihi 下班外面天氣是']
            forcastTimeZone = 3
        else:
            prefixArray = ['今天晚上天氣是', '晚上外面天氣是']
            forcastTimeZone = 4

        midfixArray = [' 氣溫是', ',溫度有', '，結果氣溫']
        subfixArray = [
            '度', '度', '度', '度，真的不是人在待的', '度, 可去外面曬曬太陽', '度, 意圖令人開冷氣', '度, 我都快熱當了!!', '', '度, 提醒@vin大大開冷氣']

        msg = random.choice(prefixArray) + weatherToday['list'][forcastTimeZone]['weather'][0][
            'description'] + random.choice(
            midfixArray) + str(int(weatherToday['list'][forcastTimeZone]['main']['temp']) - 273.15) + random.choice(
            subfixArray)
        self.send(mMessage.to, msg)

        if u"雨" in weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"多雲" in \
                weatherToday['list'][forcastTimeZone]['weather'][0]['description'] or u"晴" in \
                weatherToday['list'][forcastTimeZone]['weather'][0]['description'] and (
                    int(weatherToday['list'][forcastTimeZone]['main']['temp']) - 273.15) > 30:
            rainNoti = ['記得提醒@vin大大帶傘', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘',
                        '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！', '出門記得帶把傘', '記得要帶傘出門歐！']
            self.send(mMessage.to, random.choice(rainNoti), message_type=mMessage.type)


    # change status of speak function
    def check_modify_speak_status(self, msg):

        if not 'umbobot' in msg:
            return False

        activate_strings = ['開啟語音', '不要念']
        deactivate_strings = ['關閉語音', '念出來']

        for astring in activate_strings:
            if astring in msg:
                global speak_out
                speak_out = True
                print 'speak is turn on for keyword: ', astring
                return True

        for dstring in deactivate_strings:
            if dstring in msg:
                global speak_out
                speak_out = False
                print 'speak is turn off for keyword: ', dstring
                return True

        return False


    # in order to increase chitchat variety, bot will sometimes go off the rail and do something unexpected.
    # sendRandomMessage() insure bot will reply something meaningless occasionally.
    def checkSendRandomMessage(self):
        if random.randrange(0, 101) > 98:
            print ' **send random message'

            if random.randrange(0, 101) < 75:

                action = random.choice(self.action_list)
                while 'commonDia' in action and action['commonDia'] == False:
                    print' ***not common dialog, re-roll'
                    action = random.choice(self.action_list)

                totalMessage = random.choice(action['response'])
                response_messages = totalMessage.split('*')

                self.send_from_messages(response_messages)
                print' **random message "', response_messages, '" sended'

            else:
                if random.randrange(0, 101) > 50:
                    radReply = ['http://i.imgur.com/DJG1aF4.jpg', 'http://i.imgur.com/ggvWFBo.jpg', 'http://i.imgur.com/xovuE25.jpg',
                                'http://i.imgur.com/uSGbEFG.jpg', 'http://i.imgur.com/mAuzhW9.jpg', 'http://i.imgur.com/8J0DPac.jpg',
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg),
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg),
                                random.choice(self.histMsg), random.choice(self.histMsg), random.choice(self.histMsg)]

                    response_messages = random.choice(radReply).split('*')

                    self.send_from_messages([response_messages])

                else:
                    msg = random.choice(emoji)
                    self.send_from_messages([msg])
                    print' **random message "', msg, '" sended'

            return True

        return False


    # def antiWash(self):
    # return False
    #
    # # remove antiwash function
    #
    # if len(self.histFrom) - self.histPisiton < 7:
    # return False
    #
    # samePerson = True
    # firstPesron = self.histFrom[self.histPisiton]
    #
    # i = self.histPisiton
    # while i > 0 and i > self.histPisiton - 7:
    # if firstPesron != self.histFrom[i]:
    # print 'name', self.histFrom[i]
    # samePerson = False
    # i -= 1
    # break
    #
    # if samePerson:
    # if random.randrange(0, 101) > 75:
    # self.angry += 3
    # response = ['可以不要洗版了嗎？', '洗版很好玩嗎？', '不要為了要我回文亂發言好嗎？', '人的忍耐是有限度的！']
    #             self.send(mMessage.getFrom(), random.choice(response), message_type=mMessage.getType())
    #         else:
    #             if random.randrange(0, 101) > 80:
    #                 self.angry += 2
    #                 self.happy += 3
    #                 i = 0
    #                 for msg in self.histMsg:
    #                     self.send(mMessage.getFrom(), random.choice(self.histMsg), message_type=mMessage.getType())
    #                     i += 1
    #                     if i > 7:
    #                         return True
    #
    #     return samePerson


    def printCurrentEmotion(self):
        print '*** print emo ***'
        print 'happy: ', self.happy, 'sad: ', self.sad, 'angry level: ', self.angry
        print'*** lastCheckTime: ', self.lastCheckTime, ' ***'


    def checkIfContain(self, keyArray):
        # total key array
        for key in keyArray:
            keyArray_ = key.split('*')

            # is this a key for 'umbobot personal chat'?
            is_umbobot_key = False

            for key_ in keyArray_:
                if key_.lower() == 'umbobot':
                    is_umbobot_key = True

            message = ''
            idx = len(self.histMsg)

            if is_umbobot_key:


                print str(idx - 1 >= 0), '!!!!', str((len(self.histMsg) - 1) - idx <= MaxComprehensiveLine)

                while idx - 1 >= 0 and (len(self.histMsg) - 1) - idx <= MaxComprehensiveLine:
                    idx -= 1
                    print 'current idx: ', idx, '  msg: ', self.histMsg[idx], 'isChecked: ', self.histChecked[idx]

                    if self.histChecked[idx] == False or (len(self.histMsg[idx]) < 10 and 'umbobot' in self.histMsg[idx].lower()):
                        message = message + self.histMsg[idx]

                print 'appended message: ', message

            else:
                message = self.histMsg[len(self.histMsg) - 1]

            match_key = True

            for key_ in keyArray_:
                if key_ not in message:
                    match_key = False

            if match_key:
                global lsat_idx
                lsat_idx = idx

                return True

        return False


    # check if people speak in bad temper,
    def checkBadPeople(self, message_string):
        badEnding = [u'拉', u'啦', u'辣']
        response = ['兇屁', '你是在大聲什麼啦！', '你生氣了？？']

        idx = len(message_string) - 1
        for key in badEnding:
            if message_string[idx] == key:

                self.angry += 1
                if random.randrange(0, 101) > 50:
                    self.send(mMessage.frm, random.choice(response), message_type=mMessage.type)
                    self.hatedPeopleName = mMessage.frm._nick
                    return True
                else:
                    return False
        return False


    def updateCurrentEmotion(self, message_string):
        # decay emotion with the time passed

        currentTime = int(time.time())
        timeDiff = currentTime - self.lastCheckTime

        if self.ShowEmoLog:
            print (timeDiff), 'passed since last update'

        self.happy -= self.decayValue * timeDiff / 3600
        self.sad -= self.decayValue * timeDiff / 3600
        self.angry -= self.decayValue * timeDiff / 3600

        # reset emo if <0
        if self.angry < 0:
            self.angry = 0
        if self.sad < 0:
            self.sad = 0
        if self.happy < 0:
            self.happy = 0
        self.lastCheckTime = int(time.time())

        # update emo with new input
        if self.checkIfContain(happyString):
            if self.ShowEmoLog:
                print 'happy str matched: ' + message_string
            self.happy += 1

        if self.checkIfContain(sadString):
            if self.ShowEmoLog:
                print 'sad str matched: ' + message_string
            self.sad += 1

        if self.checkIfContain(angryString):
            if self.ShowEmoLog:
                print 'angry str matched: ' + message_string
            self.angry += 1


    def checkGogobotCmd(self, message):
        # reload all action list
        if 'umboreload' in message:
            print 'COMMDAND RECEIVED: reload action list'
            self.LastUpdateTime = 0
            self.send(mMessage.frm, 'command received, reloading', message_type=mMessage.type)

            return

        if 'umboreset' in message:
            print 'COMMDAND RECEIVED: reset memory'
            self.histFrom = []
            self.histFromNick = []
            self.histMsg = []
            self.send(mMessage.frm, 'command received, history is now clean', message_type=mMessage.type)

        if 'umboshowcompare' in message:
            if self.ShowCompareLog == True:
                self.ShowCompareLog = False
            else:
                self.ShowCompareLog = True
            print 'COMMDAND RECEIVED: ShowCompareLog set to ', self.ShowCompareLog

        if 'umboshowhist' in message:
            if self.ShowTalkHis == True:
                self.ShowTalkHis = False
            else:
                self.ShowTalkHis = True
            print 'COMMDAND RECEIVED: ShowTalkHis set to ', self.ShowCompareLog

        if 'umbotest' in message:
            self.send(mMessage.frm, '@kakashi', message_type=mMessage.type)
            print 'COMMDAND RECEIVED: gogotest'

        # if 'gogowash' in message:
        #     if self.ShowAntiWash:
        #         self.ShowAntiWash = False
        #     else:
        #         self.ShowAntiWash = True
        #
        #     self.send(mMessage.getFrom(), 'antiwash status is now :' + self.ShowAntiWash, message_type=mMessage.getType())
        #     print 'COMMDAND RECEIVED: antiwash status is now :', self.ShowAntiWash

        if 'umboremindlog' in message:

            if self.show_reminder_log:
                self.show_reminder_log = False
            else:
                self.show_reminder_log = True
            self.send(mMessage.frm, 'umboremindlog status is now :' + self.show_reminder_log,
                      message_type=mMessage.type)


    @botcmd
    def look(self, message, args):
        ''' send umbocv emoji when received command look
        '''
        self.send(message.getfrm,
                  '(umbocv)',
                  message_type=message.type)


    # def checkWantRemind(self, message):
    # if u'提醒我' in message:
    # message.replace(u'提醒我', '')
    # if u'點' in message or u'分' in message:
    # message.
    #
    #
    # else:
    # self.send(mMessage.getFrom(), random.choice(
    # '你沒說時間啊？'), message_type=mMessage.getType())
    # else:
    # return False

    def callback_message(self, message):
        # start checking thread if snot started yet
        if not self.isCheckThreadStarted:
            mThread = self.TimerThread(self)
            mThread.start()
            self.isCheckThreadStarted = True

        # ###### pre-process #######
        ask_umbobot = False
        if 'umbobot' in message.body:
            ask_umbobot = True

        message_string = re.sub("<[^>]*>:", "", message.body)
        message_from = message.frm
        message_to = message.to

        if not message_from or not message_string:
            print 'error ', message_to
            print 'error ', message_from
            print 'error ', message_string
            return

        # 阻止自言自語
        if 'umbobot' in message_from.nick or 'UmboBot' in message_from.nick:
            return

        global mMessage
        mMessage = message
        global mMessageTime
        mMessageTime = int(time.time())

        # non-umbobot response part, maybe custom umbobot command or some bug proof code.
        self.checkGogobotCmd(message_string)
        self.checkUpdateKeyword()

        self.saveHist(message_string, message_from)

        # ###### umbobot response part #######

        # random response #1
        if self.checkSendRandomMessage():
            return

        if self.check_modify_speak_status(message_string):
            return

        # do not trigger on links
        if 'http:' in message_string or 'https:' in message_string:
            self.checkSendRandomMessage()
            return

        if self.checkBadPeople(message_string):
            return

        if self.checkWeather(message_string):
            return

        # if self.ShowAntiWash and self.antiWash():
        #     return

        if self.ShowEmoLog:
            print 'emotion before update'
            self.printCurrentEmotion()
        self.updateCurrentEmotion(message_string)
        if self.ShowEmoLog:
            print 'emotion after update'
            self.printCurrentEmotion()

        if self.ShowCompareLog:
            print '*** message received, try to responese ***'
            print 'message: ', message_string

        counter = 0
        Appendedkeyword = ''

        # start to search if it match any keyword in action_list
        print '****** start to check action *****'
        for action in self.action_list:
            if self.ShowCompareLog:
                if counter < 10:
                    counter += 1
                    Appendedkeyword = Appendedkeyword + action['keyword'][0] + ", "
                else:
                    print 'check keywords: ', Appendedkeyword
                    counter = 0
                    Appendedkeyword = ' '

            if self.checkIfContain(action['keyword']):
                if self.ShowCompareLog:
                    print '"', action['keyword'][0], '" matched'

                if 'chance' in action:
                    if self.ShowCompareLog:
                        zhprint(' ** ' + ''.join(action['keyword']) + ' has roll-key, have to roll ')
                    if random.randrange(0, 101) < int(action['chance']):
                        if self.ShowCompareLog:
                            print ' **rand < ', action['chance'], ', roll success!!'
                        totalMessage = random.choice(action['response'])
                        response_messages = totalMessage.split('*')

                        self.send_from_messages(response_messages)
                        self.histChecked[len(self.histChecked) - 1] = True

                        # print 'set ',len(self.histChecked)-1 , 'to True'

                        return
                    elif self.ShowCompareLog:
                        print ' **rand > ', action['chance'], ', roll failed!'

                else:
                    totalMessage = random.choice(action['response'])
                    response_messages = totalMessage.split('*')

                    self.send_from_messages(response_messages)
                    self.histChecked[len(self.histChecked) - 1] = True

                    # print 'set ',len(self.histChecked)-1 , 'to True'

                    return

        print '****** end checking action *****'


        if self.searchResult(message_string, ask_umbobot):
            return

        # random response #2
        if self.checkSendRandomMessage():
            return

        if self.ShowCompareLog and counter != 0:
            print 'chceck keyword: ', Appendedkeyword

