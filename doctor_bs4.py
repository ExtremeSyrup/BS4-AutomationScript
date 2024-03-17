import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

Name = list()
Title = list()
Gender = list()
Expertise = list()
Research_Interests = list()
Phone = list()
Location = list()
Education = list()

def main():
	# for all the 295 Pages
	for _ in range(1, 296):
		base_url = "https://www.hopkinsmedicine.org/"
		url = base_url + "profiles/search?query=&page="+str(_)
		headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
		response = requests.get(url, headers=headers).text


		soup = BeautifulSoup(response, 'html.parser')
		# print(soup.prettify())

		# going deep into each doctor profile
		doctor_links = soup.find_all('a', class_="doctorLink heading-chevron")

		for doctor_link in doctor_links:
			print("\n")
			doctor_url = base_url + doctor_link['href']

			doctorResponse = requests.get(doctor_url, headers=headers).text
			soup2 = BeautifulSoup(doctorResponse, 'html.parser')

			# About the doctor
			about_doctor = soup2.find_all('h1')[0].text.split(',')

			# Extracting the doctor name [COLUMN 1]
			doctor_name = about_doctor[0]
			print("Name: ", doctor_name)
			Name.append(doctor_name.strip())

			# Extracting the title [COLUMN 2]
			doctor_title = ",".join(about_doctor[1:])
			print("Title: ", doctor_title)
			Title.append(doctor_title.strip())

			# Extracting the gender [COLUMN 3]
			gender_list = soup2.find_all('strong')
			gender = str()
			if len(gender_list) == 0:
				gender = '-'
				Gender.append('-')
			else:
				gender = gender_list[0].text
				if gender == 'Male' or gender == 'Female':
					Gender.append(gender)
					print("Gender: ", gender.strip())
				else:
					Gender.append('-')
			

			# Extracting Expertise [COLUMN 4]
			doctor_expertise = str()
			s = soup2.select('.read-more-wrapper')
			if len(s) != 0:
				doctor_expertise = s[0].text[:-13];
			else:
				expertise_div = soup2.find('div', class_='expertise')
				if expertise_div:
					p_element = expertise_div.find('p')

					if p_element is not None:
						expertise_text = p_element.get_text()
						doctor_expertise = expertise_text
					else:
						doctor_expertise = "-"
				else:
					doctor_expertise = '-'
			print("Expertise: ", doctor_expertise)
			Expertise.append(doctor_expertise.strip())

			# Extracting Research Interests [COLUMN 5]
			doctor_research = str()
			s = soup2.select('.research .read-more-wrapper')
			if len(s) != 0:
				doctor_research = s[0].text[:-13];
			else:
				research_div = soup2.find('div', class_='research')
				if research_div:
					p_element = research_div.find('p')

					if p_element is not None:
						research_text = p_element.get_text()
						doctor_research = research_text
					else:
						doctor_research = "-"
				else:
					doctor_research = '-'
			print("Research Interests: ", doctor_research)
			Research_Interests.append(doctor_research.strip())

			# Extracting Phone [COLUMN 6]
			cnct = str()
			phoneNos = soup2.select(".col-4-item:nth-child(2) a")
			if len(phoneNos) == 0:
				ph = soup2.select(".phone")
				if len(ph) == 0:
					cnct = '-'
				else:
					cnct = ph[0].text.strip()[7:19]
			else:
				cnct = phoneNos[0].text
			print("Phone No: ", cnct.strip())
			Phone.append(cnct)
			
			# Extracting Location [COLUMN 7]
			addr = str()
			address_div = soup2.find('div', class_='address')
			if address_div is not None:
				address_string = address_div.get_text(strip=True)
				addr = address_string
			else:
				Addr = '-'
			print("Address: ", addr[:-13])
			Location.append(addr.strip()[:-13])

			# Extracting Education [COLUMN 8]
			univs = soup2.select('#Education ul:nth-child(3) li')
			univ_str = str()
			for univ in univs:
				univ_str = univ_str + ', ' + univ.text
			print("Education: ", univ_str[2:])
			Education.append(univ_str[2:].strip())

	d = {
		'Name' : Name,
		'Title' : Title,
		'Gender' : Gender,
		'Expertise' : Expertise,
		'Research_Interests' : Research_Interests,
		'Phone' : Phone,
		'Location' : Location,
		'Education' : Education
	}

	df = pd.DataFrame(d)
	print(df)

	df.to_json('data.json', orient='records')

	with open('data.json') as file:
		data = json.load(file)

	with open('prettified_data.json', 'w') as file:
		json.dump(data, file, indent=4, sort_keys=True)
	print("TASK COMPLETED")

if __name__ == '__main__':
	main()