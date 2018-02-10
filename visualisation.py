from pprint import pprint
import requests, json
import MySQLdb

conn = MySQLdb.connect( host	= "localhost",
						user	="root",
						passwd	="",
						db		="cocktails",
						charset	='utf8')
x = conn.cursor()

if conn:
	print("Connected!")
else:
	print("Not connected!")

i=1
while True:
	url				= "http://jakidrink.pl/drink/get/"+ str(i)
	r				= requests.get(url)
	if r.status_code == 200:
		cocktails		= r.json()
		cocktail_id		= cocktails["id"]
		cocktail_name	= cocktails["name"]
		print ("----------------------")
		print ("Coctail name: {} cocktail id: {}".format(cocktail_name,cocktail_id))	#cocktail name
		components		= cocktails["components"]
		for component in components:
			component_id			= component["id"]
			component_name			= component["name"]
			component_unitShortName = component["unitShortName"]
			component_typeName		= component["componentTypeName"]
			component_volume		= component["volume"]
			print("For Cocktail: {} Id: {} add component {} to DB".format(cocktail_name,cocktail_id,component_name)) #all cocktails
			try:
				x.execute("""INSERT INTO
									cocktail(`cocktail_id`,
											`cocktail_name`,
															`component_id`,
															`component_name`,
															`component_unitShortName`,
															`component_typeName`,
															`component_volume`)
										VALUES	(%s,%s,
														%s,%s,%s,%s,%s)""",
												(cocktail_id,
												cocktail_name,
															component_id,
															component_name,
															component_unitShortName,
															component_typeName,
															component_volume,))
				conn.commit()
			except Exception as e:
				print(e)
				conn.rollback()
				conn.close()
	else:
		break
	i+=1

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
print("5 most popular ingredients:")# selected from DB
for i in data:
	print("ID:{} | Name:{} | amount:{}".format(i[0],i[1],i[2]))

#------------------------ ZADANIE 4 -----------------------------
list_of_5_components=[]
for component in data:
	list_of_5_components.append(component)

ids_of_components = []
for component_info in list_of_5_components:
	ids_of_components.append(component_info[0])

try:
	x.execute("""SELECT `cocktail_name`
					FROM cocktail one
						WHERE 5 = (SELECT SUM(1) as Count
						FROM cocktail two
						WHERE ((`component_id`='%s' OR `component_id`='%s' OR
								`component_id`='%s' OR `component_id`='%s' OR
								`component_id`='%s') AND (`one.cocktail_name` = `two.cocktail_name`))
						GROUP BY `cocktail_name`)""",
								ids_of_components[0],ids_of_components[1],
								ids_of_components[2],ids_of_components[3],
								ids_of_components[4])
	data = x.fetchall()
except Exception as e:
	print(e)
	conn.rollback()
	conn.close()

print("List of coctails you can make:")
for cocktail in data:
	print("------------>{}<----------------".format(cocktail))
#------------------------ ZADANIE 4 -----------------------------

# if you need make breakes in code to sea what is going on (start)
	# press = input("\n Press any key(0 - exit) ")
	# if press == '0':
	# 	break
# if you need make breakes in code to sea what is going on (end)