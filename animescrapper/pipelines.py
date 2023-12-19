from itemadapter import ItemAdapter
import datetime as dt
import mysql.connector
import re

# Storing Pipeline
class SaveToDB(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='aws.connect.psdb.cloud',
            user='xfroz16rd1lxpsjeh5kd',
            password='pscale_pw_DyTXiWGUofR62taIKiJ5Wtuwq1GXluj7r2ntEOhzOVK',
            database='anime'
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute(f'''SELECT EXISTS(SELECT * from anime WHERE name="{item['Name']}")''')
        exists = self.curr.fetchall()[0][0]
        if exists:
            self.curr.execute(
                f'''UPDATE anime 
                    SET Aired="{item['Aired']}", 
                        Broadcast="{item['Broadcast']}", 
                        Duration="{item['Duration']}", 
                        Status="{item['Status']}", 
                        Type="{item['Type']}", 
                        Premiered="{item['Premiered']}", 
                        Episodes="{item['Episodes']}", 
                        Rating="{item['Rating']}", 
                        Genres="{item['Genres']}", 
                        Licensors="{item['Licensors']}", 
                        Producers="{item['Producers']}", 
                        Studios="{item['Studios']}", 
                        Members="{item['Members']}", 
                        Favorites="{item['Favorites']}" 
                    WHERE name="{item['Name']}"''')
        else:
            self.curr.execute(
                f'''INSERT INTO anime (name, Aired, Broadcast, Duration, Status, Type, Premiered, Episodes, Rating, Genres, Licensors, Producers, Studios, Members, Favorites)
                    VALUES {
                        (item["Name"], 
                         item["Aired"], 
                         item["Broadcast"], 
                         item["Duration"], 
                         item["Status"], 
                         item["Type"], 
                         item["Premiered"], 
                         item["Episodes"], 
                         item["Rating"], 
                         item["Genres"], 
                         item["Licensors"], 
                         item["Producers"], 
                         item["Studios"], 
                         item["Members"], 
                         item["Favorites"],)
                        }''')
        self.conn.commit()

# Cleaning Pipeline
class AnimeItemPipeline:

    def prep_aired(self, adapter):
        if adapter.get('Aired'):
            data = adapter.get('Aired')[0]
            try:
                # Jan 26, 1990 to Oct 19, 1998
                if re.fullmatch(r"[a-zA-Z]{3} [0-9]{1,2}, [0-9]{4} to [a-zA-Z]{3} [0-9]{1,2}, [0-9]{4}", data):
                    aired = aired.split(' to ')
                    start_date = str(dt.datetime.strptime(aired[0], "%b %d, %Y").date())
                    end_date = str(dt.datetime.strptime(aired[1], "%b %d, %Y").date())
                    aired = ','.join([start_date, end_date])

                # Mar 2021
                elif re.match(r"[a-zA-Z]{3} [0-9]{4}", data):
                    aired = str(dt.datetime.strptime(data, "%b %Y").date())

                # 1989-06-05 1989-12-05
                elif re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{4}-[0-9]{2}-[0-9]{2}", data): 
                    aired = 'none'

                # 2021
                elif re.fullmatch(r"([0-9]{4})", data): 
                    aired = str(dt.datetime.strptime(data, "%Y").date())

                # 2006 to 2009
                elif re.fullmatch(r"[0-9]{4} to [0-9]{4}", data):
                    aired = data.split(' to ')
                    start_date = str(dt.datetime.strptime(aired[0], "%Y").date())
                    end_date = str(dt.datetime.strptime(aired[1], "%Y").date())
                    aired = ','.join([start_date, end_date])

                # Dec 30, 2016 to ?
                elif re.match(r"[a-zA-Z]{3} [0-9]{1,2}, [0-9]{4} to \?", data): 
                    aired = str(dt.datetime.strptime(data, "%b %d, %Y to ?").date())

                # b
                elif re.match(r"[a-z]", data): 
                    aired = 'none'

                # Jan 26, 1990 to Oct 1998
                elif re.match(r"[a-zA-Z]{3} [0-9]{1,2}, [0-9]{4} to [a-zA-Z]{3} [0-9]{4}", data): 
                    aired = data.split(' to ')
                    start_date = str(dt.datetime.strptime(aired[0], "%b %d, %Y").date())
                    end_date = str(dt.datetime.strptime(aired[1], "%b %Y").date())
                    aired = ','.join([start_date, end_date])
                
                # Feb 11, 2001 to 2001
                elif re.match(r"[a-zA-Z]{3} [0-9]{1,2}, [0-9]{4} to [0-9]{4}", data):
                    aired = data.split(' to ')
                    start_date = str(dt.datetime.strptime(aired[0], "%b %d, %Y").date())
                    end_date = str(dt.datetime.strptime(aired[1], "%Y").date())
                    aired = ','.join([start_date, end_date])
                else:
                    return str(data)
                
                return aired
            except:
                return str(data)
        return 'none'
    
    def prep_producers(self, adapter):
        if adapter.get('Producers'):
            producers = adapter.get('Producers')
            if 'add some' in producers[0] or 'add some' in producers:
                producers = 'none'
                return producers
            producers = ','.join(producers)
            return producers
        else:
            return 'none'
    
    def prep_licensors(self, adapter):
        if adapter.get('Licensors'):
            licensors = adapter.get('Licensors')
            if 'add some' in licensors[0] or 'add some' in licensors:
                licensors = 'none'
                return licensors
            licensors = ','.join(licensors)
            return licensors
        else:
            return 'none'
    
    def prep_episodes(self, adapter):
        if adapter.get('Episodes'):
            try:
                episodes = adapter.get('Episodes')[0]
                return int(episodes)
            except:
                return 0
        else:
            return 0
    
    def prep_duration(self, adapter):
        if adapter.get('Duration'):
            duration = adapter.get('Duration')[0]
            try:
                # 23 min. per ep.
                if 'per ep' in duration:
                    duration = dt.datetime.strptime(duration, '%M min. per ep.')
                    return str(duration.time())
                # 1 hr. 36 min.
                elif 'hr' in duration and 'min' in duration:
                    duration = dt.datetime.strptime(duration, '%I hr. %M min.')
                    return str(duration.time())
                # 1 hr.
                elif 'hr' in duration:
                    duration = dt.datetime.strptime(duration, '%I hr.')
                    return str(duration.time())
                # 36 min.
                elif 'min' in duration:
                    duration = dt.datetime.strptime(duration, '%M min.')
                    return str(duration.time())
                else:
                    return str(duration)
            except:
                return str(duration)
        else:
            return 'none'
            
    def prep_broadcast(self, adapter):
        if adapter.get('Broadcast'):
            data = adapter.get('Broadcast')[0]
            days = {
                    "Mondays": 'mon', 
                    "Tuesdays": 'tue', 
                    "Wednesdays": 'wed',
                    "Thursdays": 'thur', 
                    "Fridays": 'fri', 
                    "Saturdays": 'sat', 
                    "Sundays": 'sun'
                }
            # try:
            if re.match(r"[a-zA-Z]* at [0-9]{2}:[0-9]{2} \(JST\)", data):
                broadcast = data.split(' ')
                weekday = days[broadcast[0]]
                time = dt.datetime.strptime(broadcast[2], '%H:%M')
                broadcast = str(weekday) + ',' + str(time.time())
            elif data == 'None' or data == 'Unknown' or data == 'Not scheduled once per week' or re.fullmatch(r"[a-z]",data):
                broadcast = 'none'
            elif re.match(r"[0-9],? ?\d*:\d*:\d*", data):# 5 01:40:00
                broadcast = 'none'
            elif re.match(r"[a-zA-Z]* at Unknown", data):# Saturdays at Unknown
                broadcast = data.split(' at ')
                broadcast = days[broadcast[0]]
            else:
                return data
            return broadcast
            # except:
            #     return data
        else:
            return 'none'
        
    def prep_rating(self, adapter):
        if adapter.get('Rating'):
            rating = adapter.get('Rating')[0]
            if 'Teens' in rating:
                return 'PG 13'
            elif 'violence' in rating:
                return 'R 17'
            elif 'Nudity' in rating:
                return 'R+'
            elif 'Children' in rating:
                return 'PG'
            elif 'All' in rating:
                return 'G'
            else:
                return rating
        else:
            return 'none'
    
    def prep_members(self, adapter):
        if adapter.get('Members'):
            members = adapter.get('Members')[0]
            members = members.replace(',', '')
            return int(members)
        else:
            return 'none'
        
    def prep_favs(self, adapter):
        if adapter.get('Favorites'):
            favs = adapter.get('Favorites')[0]
            favs = favs.replace(',', '')
            return int(favs)
        else:
            return 'none'
    
    def prep_premiered(self, adapter):
        if adapter.get('Premiered'):
            return adapter.get('Premiered')[0]
        else:
            return 'none'
        
    def prep_genres(self, adapter):
        if adapter.get('Genres'):
            genre = adapter.get('Genres')
            genre = ','.join(genre)
            return genre
        else:
            return 'none'
        
    def prep_studios(self, adapter):
        if adapter.get('Studios'):
            studio = adapter.get('Studios')
            if 'add some' in studio[0] or 'add some' in studio:
                studio = 'none'
                return studio
            studio = ','.join(studio)
            return studio
        else:
            return 'none'
        
    def prep_status(self, adapter):
        if adapter.get('Status'):
            status = adapter.get('Status')[0]
            return status
        else:
            return 'none'
    
    def prep_type(self, adapter):
        if adapter.get('Type'):
            type = adapter.get('Type')[0]
            return type
        else:
            return 'none'
        
    def prep_name(self, adapter):
        if adapter.get('Name'):
            name = adapter.get('Name')
            name = name.replace('"', '').replace("'", '')
            return name
        else:
            return 'none'


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['Aired'] = self.prep_aired(adapter)
        adapter['Producers'] = self.prep_producers(adapter)
        adapter['Licensors'] = self.prep_licensors(adapter)
        adapter['Episodes'] = self.prep_episodes(adapter)
        adapter['Duration'] = self.prep_duration(adapter)
        adapter['Broadcast'] = self.prep_broadcast(adapter)
        adapter['Rating'] = self.prep_rating(adapter)
        adapter['Members'] = self.prep_members(adapter)
        adapter['Favorites'] = self.prep_favs(adapter)
        adapter['Premiered'] = self.prep_premiered(adapter)
        adapter['Genres'] = self.prep_genres(adapter)
        adapter['Studios'] = self.prep_studios(adapter)
        adapter['Status'] = self.prep_status(adapter)
        adapter['Type'] = self.prep_type(adapter)
        adapter['Name'] = self.prep_name(adapter)

        return item
