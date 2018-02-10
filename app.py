from pprint import pprint
import requests, json
import MySQLdb
import MySQLdb.cursors as cursors

conn = MySQLdb.connect( host	= "localhost",
						user	="root",
						passwd	="",
						db		="cocktails",
						charset	='utf8')
x = conn.cursor()

# i=1
# while True:
# 	url				= "http://jakidrink.pl/drink/get/" + str(i)
# 	r				= requests.get(url)
# 	if r.status_code == 200:
# 		cocktails		= r.json()
# 		cocktail_id		= cocktails["id"]
# 		cocktail_name	= cocktails["name"]
# 		components		= cocktails["components"]
# 		for component in components:
# 			component_id			= component["id"]
# 			component_name			= component["name"]
# 			component_unitShortName = component["unitShortName"]
# 			component_typeName		= component["componentTypeName"]
# 			component_volume		= component["volume"]
# 			try:
# 				x.execute("""INSERT INTO
# 									cocktail(`cocktail_id`,
# 											`cocktail_name`,
# 															`component_id`,
# 															`component_name`,
# 															`component_unitShortName`,
# 															`component_typeName`,
# 															`component_volume`)
# 										VALUES	(%s,%s,
# 														%s,%s,%s,%s,%s)""",
# 												(cocktail_id,
# 												cocktail_name,
# 															component_id,
# 															component_name,
# 															component_unitShortName,
# 															component_typeName,
# 															component_volume,))
# 				conn.commit()
# 			except Exception as e:
# 				print(e)
# 				conn.rollback()
# 				conn.close()
# 	else:
# 		break
# 	i+=1

try:
	x.execute("""(SELECT `component_id`,`component_name`, count(`component_id`)
					FROM cocktail
					WHERE (`component_typeName`='alkohol' OR `component_typeName`='likier')
					GROUP BY `component_id`
					ORDER BY count(`component_id`) DESC LIMIT 2)
			UNION ALL
				(SELECT `component_id`,`component_name`, count(`component_id`)
					FROM cocktail
					WHERE (`component_typeName`<>'alkohol' AND `component_typeName`<>'likier')
					GROUP BY `component_id`
					ORDER BY count(`component_id`) DESC LIMIT 3)""")
	data = x.fetchall()
except Exception as e:
	print(e)
	conn.rollback()
	conn.close()

list_of_5_components=[]
for component in data:
	list_of_5_components.append(component)

ids_of_components = []
for component_info in list_of_5_components:
	ids_of_components.append(component_info[0])

try:
	x.execute("""SELECT `cocktail_name`
				FROM cocktail one
				WHERE 5 = (SELECT SUM(1) as total
				FROM cocktail two
				WHERE `two`.`cocktail_name` = `one`.`cocktail_name` AND `component_id` IN (%s,%s,%s,%s,%s)
				GROUP BY `cocktail_name`);""",
								ids_of_components[0],ids_of_components[1],
								ids_of_components[2],ids_of_components[3],
								ids_of_components[4])
	data = x.fetchall()
except Exception as e:
	print(e)
	conn.rollback()
	conn.close()

list_of_cocktails=[]
for cocktail_info in data:
	list_of_cocktails.append(cocktail_info)

names_of_cocktails = []
for coctail in list_of_cocktails:
	names_of_cocktails.append(coctail[1])

print("List of cocktails:")
for cocktail in names_of_cocktails:
	print("{}".format(cocktail))