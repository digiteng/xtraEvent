# -*- coding: utf-8 -*-
# by digiteng...03.2024-2026

from __future__ import absolute_import
from time import time, localtime, strftime
import socket
from Components.config import config, configfile
import re, os
from math import floor, log
bbb=""
MAC = None
MAC = os.popen("ifconfig eth0 | awk '/HWaddr/ {printf $5}'").read()
headers_v = {"X-Api-Key": MAC}

skin_ATV_TMDB_1 = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/skins/ATV/ATV_TMDB_1.xml"
skin_ATV_TMDB_2 = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/skins/ATV/ATV_TMDB_2.xml"
skin_ATV_TMDB_3 = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/skins/ATV/ATV_TMDB_3.xml"
skin_ATV_IMDB_1 = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/skins/ATV/ATV_IMDB_1.xml"
skin_ATV_IMDB_2 = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/skins/ATV/ATV_IMDB_2.xml"
skin_AI = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/skins/AI.xml"

noActPic = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/noAct.png"
noBacdrop = "/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/pic/film3.jpg"
msg_2 = "\c00ff8800 \n \c00ef4c4c No Internet Connection !!!"
lang = config.plugins.xtrvnt.searchLang.value
trailer_res = "720p"
xaaa=""
img = "/etc/issue"
if os.path.exists(img):
	with open(img, "r") as f:
		imgr = f.read().lower()

REGEX = re.compile(
	# r"-.*|"
	r"([\(\[]).*?([\)\]])|"
	r"(: odc.\d+)|"
	r"(\d+: odc.\d+)|"
	r"(\d+ odc.\d+)|(:)|"
	r"(\d+.* \(odc. \d+.*\))|"
	r"!|"
	r"/.*|"
	r"\|\s[0-9]+\+|"
	r"[0-9]+\+|"
	# r"\s\d{4}\Z|"
	r"([\(\[\|].*?[\)\]\|])|"
	# r'(\"|\"\.|\"\,|\.)\s.+|'
	r"\"|:|"
	r"\*|"
	r"Премьера\.\s|"
	r"(х|Х|м|М|т|Т|д|Д)/ф\s|"
	r"(х|Х|м|М|т|Т|д|Д)/с\s|"
	r"\s(с|С)(езон|ерия|-н|-я)\s.+|"
	r"\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|"
	r"\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|"
	r"\s(ч|ч\.|с\.|с)\s\d{1,3}.+|"
	r"\d{1,3}(-я|-й|\sс-н).+|",
	re.DOTALL,
)

header = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}

tmdb_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYzNlZmNmNDdjMzU3NzU1ODgxMmJiOWQ2NDAxOWQ2NSIsIm5iZiI6MTU3NDc5MzkyNS4zNjgsInN1YiI6IjVkZGQ3MmM1YTgwNjczMDAxMjEzOGY5NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.eT2nrH36Dz2bReAqLUHqV2eOGCA5dVZFig1CAhekGCQ"

headers_tmdb_token = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
	"accept": "application/json",
	"Authorization": f"Bearer {tmdb_token}"
}

downLoc = None
if config.plugins.xtrvnt.loc.value:
	downLoc = f"{config.plugins.xtrvnt.loc.value}xtraEvent"
else:
	downLoc = None

def pathLocation():
	try:
		return config.plugins.xtrvnt.loc.value
	except:
		return "/"
try:
	pathLoc = config.plugins.xtrvnt.loc.value
except:pass

def errorlog(err, file, line):
	with open("/tmp/xtraError.log", "a+") as f:
		f.write(
			f'[{strftime("%Y-%m-%d %H:%M:%S")}] [ERROR] : {err}, Line:{line}, File : {file}, \n\n'
		)

def eventlog(filex):
	with open("/tmp/xtraEvent.log", "a+") as f:
		f.write(f'{filex}\n')

def intCheck():
	try:
		socket.setdefaulttimeout(2)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
		config.plugins.xtrvnt.checkNet.value = True
		config.plugins.xtrvnt.checkNet.save()
		configfile.save()
		return True
	except:
		config.plugins.xtrvnt.checkNet.value = False
		config.plugins.xtrvnt.checkNet.save()
		configfile.save()
		return False

def getLanguage():
	lang = "en"
	try:
		from Components.Language import language
		lang = language.getLanguage()
	except:
		try:
			lang = config.osd.language.value
		except:
			lang = "en"
	return lang[:2]

def version():
	ver = "N/A"
	with open("/usr/lib/enigma2/python/Plugins/Extensions/xtraEvent/version", "r") as f:
		ver = f.read()
	return ver

def calculater(path):
	totc = 0
	totb = 0
	for a, b, c in os.walk(path):
		for d in c:
			dy = os.path.join(a, d)
			if os.path.isfile(dy):
				totc += 1
				totb += os.path.getsize(dy)
	tott = totb / (1024 * 1024)
	return totc, f"{tott:.2f} MB"

def getStorage():
	try:
		TOTAL, TMDB_total, IMDB_total,strg_total, diskSize, diskFree, diskUsed, percent_used = None,None,None,None,None,None,None,None
		white="\c00??????";grey="\c00bbbbbb"
		tot = calculater(downLoc)
		TOTAL = f"{white}TOTAL : {grey}{tot[0]} item {tot[1]}"
		tt = calculater(f"{downLoc}/tmdb")
		TMDB_total = f"{white}TMDB TOTAL : {grey}{tt[0]} item {tt[1]}"
		it = calculater(f"{downLoc}/imdb")
		IMDB_total = f"{white}IMDB TOTAL : {grey}{it[0]} item {it[1]}"
		
		stat = os.statvfs("/")
		diskSize = stat.f_blocks * stat.f_frsize
		diskFree = stat.f_bfree * stat.f_frsize
		diskUsed = diskSize - diskFree
		percent_used = (100 * (stat.f_blocks - stat.f_bfree )) // stat.f_blocks
		return TOTAL, TMDB_total, IMDB_total, diskSize, diskFree, diskUsed, percent_used
	except Exception as err:
		errorlog(err, __file__, err.__traceback__.tb_lineno)

def formatNumber(x):
	mutlak_sayi = abs(x)
	if mutlak_sayi < 1000:
		return str(x)
	birimler = [
		(1000000000, 'G'),	# Giga / Milyar
		(1000000, 'M'),		# Milyon
		(1000, 'K')			# Kilo / Bin
	]
	for bolen, birim in birimler:
		if mutlak_sayi >= bolen:
			deger = x / bolen

			if abs(deger) < 10:

				return f"{deger:.1f}{birim}".replace('.0', '')

			else:
				return f"{int(deger)}{birim}"

def formatDuration(secs):
	try:
		h = m = ""
		dur = int(secs) // 60
		hours = dur // 60
		if hours >= 1:
			h = f"{hours}h"
		minutes = dur % 60
		if minutes >= 1:
			m = f"{minutes}m"
		duration = f"{h} {m}"
		return duration
	except:pass

def sizeX(size):
	power = 0 if size <= 0 else floor(log(size, 1024))
	return f"{round(size / 1024**power, )} {['B', 'KB', 'MB', 'GB', 'TB'][int(power)]}"

def roundX(num):
	power = 0 if num <= 0 else floor(log(num, 1000))
	return f"{round(num / 1000**power, 1)} {['Bbps', 'Kbps', 'Mbps', 'Gbps', 'Tbps'][int(power)]}"

def roundXs(num):
	power = 0 if num <= 0 else floor(log(num, 1000))
	return f"{round(num / 1000**power, 2)}{['B', 'K', 'M', 'G', 'T'][int(power)]}"

def pRating(rate):
	rate = str(rate).strip()
	if rate.startswith("-") and rate[1:].isdigit():
		rate = rate.replace("-", "")

	if rate in ["G", "TV-G", "PG", "TV-Y", "TV-PG", "E", "U", "Tout Public"]:
		rate = "0"
	elif rate in ["4", "6", "6+", "7", "7A", "7+", "8", "8+", "9", "9+", "TV-Y7"]:
		rate = "6"
	elif rate in [
		"TV-14", "PG-13", "E10+", "T", "T+", "10", "10+", "11", "11+", 
		"12", "12+", "12A", "13", "13+", "13A", "14", "14+", "14A"
	]:
		rate = "12"
	elif rate in ["R", "TV-MA", "M", "15", "15+", "16", "16+", "16A"]:
		rate = "16"
	elif rate in ["NC-17", "AO", "MAX", "18", "18+", "X", "R18", "Interdit -18"]:
		rate = "18"
	else:
		if rate == "TP":
			rate = "0"
		else:
			rate = "NA"
	return rate

circle_texts = {
	0: " ",
	1: "",
	2: "",
	3: "",
	4: "",
	5: "",
	6: "",
	7: "",
	8: "",
	9: "",
	10: "",
	11: "",
	12: "",
	13: "",
	14: "",
	15: "",
	16: "",
	17: "",
	18: "",
	19: "",
	20: "",
	21: "",
	22: "",
	23: "",
	24: "",
	25: "",
	26: "",
	27: "",
	28: "",
	29: "",
	30: "",
	31: "",
	32: "",
	33: "",
	34: "",
	35: "",
	36: "",
	37: "",
	38: "",
	39: "",
	40: "",
	41: "",
	42: "",
	43: "",
	44: "",
	45: "",
	46: "",
	47: "",
	48: "",
	49: "",
	50: "",
	51: "",
	52: "",
	53: "",
	54: "",
	55: "",
	56: "",
	57: "",
	58: "",
	59: "",
	60: "",
	61: "",
	62: "",
	63: "",
	64: "",
	65: "",
	66: "",
	67: "",
	68: "",
	69: "",
	70: "",
	71: "",
	72: "",
	73: "",
	74: "",
	75: "",
	76: "",
	77: "",
	78: "",
	79: "",
	80: "",
	81: "",
	82: "",
	83: "",
	84: "",
	85: "",
	86: "",
	87: "",
	88: "",
	89: "",
	90: "",
	91: "",
	92: "",
	93: "",
	94: "",
	95: "",
	96: "",
	97: "",
	98: "",
	99: "",
	100: "",
}

checkTV = [
	"serial",
	"series",
	"serie",
	"serien",
	"série",
	"séries",
	"serious",
	"folge",
	"episodio",
	"episode",
	"épisode",
	"l'épisode",
	"ep.",
	"staffel",
	"soap",
	"doku",
	"tv",
	"talk",
	"show",
	"news",
	"factual",
	"entertainment",
	"telenovela",
	"dokumentation",
	"dokutainment",
	"documentary",
	"informercial",
	"information",
	"sitcom",
	"reality",
	"program",
	"magazine",
	"mittagsmagazin",
	"т/с",
	"м/с",
	"сезон",
	"с-н",
	"эпизод",
	"сериал",
	"серия",
	"spor",
	"sport",
	"sportschau",
]
checkMovie = [
	"film",
	"movie",
	"фильм",
	"кино",
	"ταινία",
	"película",
	"cinéma",
	"cine",
	"cinema",
	"filma",
]

xFolders = [
	"tmdb/poster",
	"tmdb/banner",
	"tmdb/backdrop",
	"tmdb/backdropThumbnails",
	"tmdb/infos",
	"mSearch",
	"EMC",
	"tmdb/casts",
	"tmdb/logos",
	"imdb",
	"imdb/backdropThumbnails",
	"youtubeThumbnails",
	"AI",
]

BASE_URL_IMDB = "https://caching.graphql.imdb.com/"

def getPayload(imdb_id):
  payload = {
	  "query": """query GetTitle($id: ID!) {
					title(id: $id) {
						id
						titleText { text }
						originalTitleText { text }
						titleType { text id }
						releaseYear { year }
						releaseDate { day month year }
						runtime { seconds }
						ratingsSummary { aggregateRating voteCount }
						metacritic { metascore { score } }
						genres { genres { text id } }
						plot {
							plotText { plainText }
							language { id }
						}
						primaryImage { url width height caption { plainText } }
						imageCount: images { total }
						videoCount: videos { total }
						principalCredits {
							category { text id }
							credits {
								name { id nameText { text } primaryImage { url } }
								... on Cast { characters { name } }
								attributes { text }
							}
						}
						certificate { rating country { text } }
						spokenLanguages { spokenLanguages { text id } }
						countriesOfOrigin { countries { text id } }
						productionStatus { currentProductionStage { text id } }
						canHaveEpisodes
						series { series { id titleText { text } releaseYear { year } } }
						episodes { episodes { total } }
						companyCredits {
							edges { node { company { id companyText { text } } category { text } } }
						}
						technicalSpecifications {
							soundMixes { items { text } }
							aspectRatios { items { aspectRatio } }
							colorations { items { text } }
						}
						akas { edges { node { text country { text } } } }
						meterRanking { currentRank rankChange { changeDirection difference } }
						keywords { edges { node { text } } }
						latestTrailer {
							id
							name { value }
							thumbnail { url }
							runtime { value }
							playbackURLs { displayName { value } url }
							contentType { displayName { value } }
							createdDate
						}
						reviews(first: 1) { total }
						connections {
							edges { node { associatedTitle { id titleText { text } releaseYear { year } } category { text } } }
						}
						moreLikeThisTitles(first: 5) {
							edges {
								node { id titleText { text } releaseYear { year } ratingsSummary { aggregateRating } primaryImage { url } }
							}
						}
						canRate { isRatable }
						isAdult
						nominations { total }
						imageGallery: images(first: 5) {
							edges { node { url caption { plainText } width height } }
						}
						trivia(first: 3) { edges { node { text { plainText } } } }
						goofs(first: 3) { edges { node { text { plainText } } } }
					}
				}""",
	  "operationName": "GetTitle",
	  "variables": {"id": imdb_id},
  }
  return payload

def GetPersonPayload(person_id):
	payload = {
		"query": """
	query GetPersonInfo($id:ID!){name(id:$id){id
	nameText{text}
	birthDate{date}
	deathDate{date}
	birthLocation{text}
	height{measurement{value
	unit}}
	bio{text{plainText}}
	primaryProfessions{category{text}}
	primaryImage{url
	width
	height}
	akas(first:3){edges{node{text}}}
	knownFor(first:3){edges{node{title{id
	titleText{text}
	releaseYear{year}
	titleType{text}
	ratingsSummary{aggregateRating}
	primaryImage{url
	width
	height}
	}}}}
	awardNominations(first: 10, filter: { wins: WINS_ONLY }) {
	edges {node {award {text
	event {text}
	category {text}
	year}}}}
	quotes(first:3){edges{node{text{plainText}}}}
	meterRanking{currentRank rankChange{changeDirection difference}}
	credits(first:5){edges{node{title{titleText{text}}}}}}}
	""",
		"variables": {"id": person_id},
	}
	return payload

genres={'28': 'Action', '12': 'Abenteuer', '16': 'Animation', '35': 'Komödie', '80': 'Krimi', '99': 'Dokumentarfilm', '18': 'Drama', '10751': 'Familie', '14': 'Fantasy', '36': 'Historie', '27': 'Horror', '10402': 'Musik', '9648': 'Mystery', '10749': 'Liebesfilm', '878': 'Science Fiction', '10770': 'TV-Film', '53': 'Thriller', '10752': 'Kriegsfilm', '37': 'Western', '10759': 'Action & Adventure', '10762': 'Kids', '10763': 'News', '10764': 'Reality', '10765': 'Sci-Fi & Fantasy', '10766': 'Soap', '10767': 'Talk', '10768': 'War & Politics'}

import requests
def sendMessageTelegram(message=None):
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	token = config.plugins.xtrvnt.telegram_token.value
	chat_id = config.plugins.xtrvnt.telegram_chatid.value

	data = {
		'chat_id': chat_id,
		'text': message
	}

	try:
		url = f'https://api.telegram.org/bot{token}/sendMessage'
		response = requests.post(url, headers=headers, data=data, timeout=10)
		return response.json()
	except Exception as e:
		return None

from enigma import eLabel, gFont, eSize, ePoint
import re
from skin import parseColor

def text_format(parent_screen, start_x, start_y, max_width, max_height, rich_text, align="left", default_font="Regular", default_size=14, default_color="00ffffff"):
	"""
			text = "|c:00ffffff|f:Bold|s:24Marlon Brando\n|c:00bbbbbb|f:Regular|s:14 Don Vito Corleone\n |c:0000ffff|f:italic|s:14abcnsnsıckzslnckzn"
			
			ttt = text_format(
				parent_screen=self,
				start_x=50, 
				start_y=100, 
				max_width=500,
				max_height=150,	
				rich_text=text,
				align="left",
				default_font="Regular",
				default_size=14
			)

			self['info'].setText(ttt);self['info'].show()
	"""
	if not hasattr(parent_screen, "rich_labels"):
		parent_screen.rich_labels = []
		
	# Eğer parent_screen bir Renderer ise ve instance'ı varsa C++ pointer'ını al
	# Renderer nesnelerinde bazen parent_screen.instance yerine doğrudan parent_screen kullanılır
	if hasattr(parent_screen, "instance") and parent_screen.instance:
		widget_parent = parent_screen.instance
	else:
		widget_parent = parent_screen

	# 2. Metni etiketlere, kelimelere, boşluklara ve satır başlarına nizami ayır (\n dahil)
	pattern = r"(\|c:[0-9a-fA-F]{8}|\|f:[^|]+|\|s:[0-9]+|\n|[^\s|]+|\s+)"
	tokens = re.findall(pattern, rich_text)
	
	current_color = default_color
	current_font = default_font
	current_size = default_size
	
	# Satırları organize etmek için geçici liste
	lines = []
	current_line_words = []
	
	# Adım A: Kelimelerin boyutlarını hesapla ve satırlara böl
	for token in tokens:
		if not token:
			continue
		if token.startswith("|c:"):
			current_color = token.replace("|c:", "")
		elif token.startswith("|f:"):
			current_font = token.replace("|f:", "")
		elif token.startswith("|s:"):
			current_size = int(token.replace("|s:", ""))
		elif token == "\n":
			lines.append(current_line_words)
			current_line_words = []
		else:
			# Kelime genişliğini harf genişliğine göre hesapla (ortalama 0.58 çarpan + güvenlik)
			is_space = token.isspace()
			if is_space:
				word_width = len(token) * int(current_size * 0.25) # Boşluklar daha dar olmalı
			else:
				word_width = int(len(token) * (current_size * 0.58)) + 6
				
			word_info = {
				"text": token,
				"font": current_font,
				"size": current_size,
				"color": current_color,
				"width": word_width,
				"is_space": is_space
			}
			current_line_words.append(word_info)
			
	if current_line_words:
		lines.append(current_line_words)

	# Adım B: Satırları Ekrana Çiz ve Hizala (Left, Center, Right)
	current_y = start_y
	
	for line in lines:
		if not line: # Boş satır (\n\n durumu için)
			current_y += int(default_size * 1.5)
			continue
			
		# Bu satırdaki en büyük font boyutu satır yüksekliği olur
		max_font_in_line = max([w["size"] for w in line])
		line_height = int(max_font_in_line * 1.5)
		
		# Satır yüksekliği max_height sınırını aşarsa çizimi durdur
		if (current_y + line_height) > (start_y + max_height):
			break
			
		# Satırın toplam genişliğini hesapla
		total_line_width = sum([w["width"] for w in line])
		
		# Hizalama (Align) başlangıç X noktasını belirler
		if align == "center":
			line_start_x = start_x + int((max_width - total_line_width) / 2)
		elif align == "right":
			line_start_x = start_x + (max_width - total_line_width)
		else: # left
			line_start_x = start_x
			
		word_x = line_start_x
		
		# Kelimeleri tek tek C++ objesi olarak ekrana bas
		for w in line:
			# Boşluk karakterlerini eLabel olarak çizmeye gerek yok, sadece X koordinatını kaydır
			if w["is_space"]:
				word_x += w["width"]
				continue
				
			if parent_screen.instance:
				lbl = eLabel(parent_screen.instance) 
			else:
				lbl = eLabel(parent_screen)
			
			lbl.setText(w["text"])
			lbl.setFont(gFont(w["font"], w["size"]))
			lbl.setForegroundColor(parseColor(f"#{w[ 'color' ]}"))
			lbl.setTransparent(1)
			
			if hasattr(eLabel, "alignCenter"):
				lbl.setVAlign(eLabel.alignCenter) # Dikey ortalama sabitleyici
				
			lbl.resize(eSize(int(w["width"]), int(line_height)))
			lbl.move(ePoint(int(word_x), int(current_y)))
			lbl.show()
			
			parent_screen.rich_labels.append(lbl)
			word_x += w["width"]
			
		# Bir sonraki satıra geç
		current_y += line_height



