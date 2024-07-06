import PyPDF2 
import pyttsx3 

path = open('sample.pdf', 'rb') 

pdfReader = PyPDF2.PdfReader(path) 

start_from = pdfReader.pages[5] 

text = start_from.extract_text() 

speak = pyttsx3.init() 
speak.say(text) 
speak.runAndWait()