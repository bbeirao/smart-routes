## Information
Application to find the optimal mapping of trucks to cargos to minimize the overall distances the trucks must travel .

## Project
Django 1.11.21.

Python 3.7

#### Run main

Execute in main folder:
	
	python main.py

#### Show two Results

## Complete Result

	[
	  {
		'cargo': [
		  'Light bulbs',
		  'Sikeston',
		  'MO',
		  '36.876719',
		  '-89.5878579',
		  'Grapevine',
		  'TX',
		  '32.9342919',
		  '-97.0780654'
		],
		'truck': [
		  'Viking Products Of Austin Incustin',
		  'Fort Campbell',
		  'TN',
		  '36.6634467',
		  '-87.47739020000002'
		]
	  },
	  {
		'cargo': [
		  'Recyclables',
		  'Christiansburg',
		  'VA',
		  '37.1298517',
		  '-80.4089389',
		  'Apopka',
		  'FL',
		  '28.6934076',
		  '-81.5322149'
		],
		'truck': [
		  'Ricardo Juradoacramento',
		  'Covesville',
		  'VA',
		  '37.8901411',
		  '-78.70474010000001'
		]
	  },
	  {
		'cargo': [
		  'Apples',
		  'Columbus',
		  'OH',
		  '39.9611755',
		  '-82.99879419999999',
		  'Woodland',
		  'CA',
		  '38.67851570000001',
		  '-121.7732971'
		],
		'truck': [
		  "Kjellberg'S Carpet Oneuffalo",
		  'Mount Vernon',
		  'OH',
		  '40.3933956',
		  '-82.4857181'
		]
	  },
	  {
		'cargo': [
		  'Cell phones',
		  'Hickory',
		  'NC',
		  '35.7344538',
		  '-81.3444573',
		  'La Pine',
		  'OR',
		  '43.67039949999999',
		  '-121.503636'
		],
		'truck': [
		  'Paul J Krez Companyorton Grove',
		  'Forest City',
		  'NC',
		  '35.3340108',
		  '-81.8651028'
		]
	  },
	  {
		'cargo': [
		  'Oranges',
		  'Fort Madison',
		  'IA',
		  '40.6297634',
		  '-91.31453499999999',
		  'Ottawa',
		  'IL',
		  '41.3455892',
		  '-88.8425769'
		],
		'truck': [
		  'Fish-Bones Towingew York',
		  'Monroe',
		  'WI',
		  '42.60111939999999',
		  '-89.6384532'
		]
	  },
	  {
		'cargo': [
		  'Wood',
		  'Hebron',
		  'KY',
		  '39.0661472',
		  '-84.70318879999999',
		  'Jefferson',
		  'LA',
		  '29.96603709999999',
		  '-90.1531298'
		],
		'truck': [
		  'Wisebuys Stores Incouverneur',
		  'Washington',
		  'WV',
		  '39.244853',
		  '-81.6637765'
		]
	  },
	  {
		'cargo': [
		  'Wood',
		  'Northfield',
		  'MN',
		  '44.4582983',
		  '-93.161604',
		  'Waukegan',
		  'IL',
		  '42.3636331',
		  '-87.84479379999999'
		],
		'truck': [
		  'Gary Lee Wilcoxpencer',
		  'Eagle River',
		  'WI',
		  '45.9171763',
		  '-89.2442988'
		]
	  }
	]

## Simple Result

	[
	  {
		'cargo': 'Light bulbs',
		'truck': 'Viking Products Of Austin Incustin'
	  },
	  {
		'cargo': 'Recyclables',
		'truck': 'Ricardo Juradoacramento'
	  },
	  {
		'cargo': 'Apples',
		'truck': "Kjellberg'S Carpet Oneuffalo"
	  },
	  {
		'cargo': 'Cell phones',
		'truck': 'Paul J Krez Companyorton Grove'
	  },
	  {
		'cargo': 'Oranges',
		'truck': 'Fish-Bones Towingew York'
	  },
	  {
		'cargo': 'Wood',
		'truck': 'Wisebuys Stores Incouverneur'
	  },
	  {
		'cargo': 'Wood',
		'truck': 'Gary Lee Wilcoxpencer'
	  }
	]
	
### Project tests
	
	test_process - Tests all process
	test_different_cargo - Test with different cargos. Cargo.csv contains cargos to simulate two cargos in the same pickup locations.
	test_build_final_list - Test simple final list.
	test_cargo_file_error - Test errors when opening cargo file.
	test_truck_file_error - Test errors when opening truck file.
	test_url_error - Test errors when loading the Google API url.

### Improvements:

The mean of project was just resolve the problem with good code and basics tests. There are many changes to do in project architecture like:  

- Enviroment variables.
- Database.
- Tests cases.
- Errors handling.
- Venv.
- And others best practices.



