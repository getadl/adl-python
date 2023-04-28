import string

constants = {
	"ascii_letters" : lambda: string.ascii_letters,
	"ascii_lowercase" : lambda: string.ascii_lowercase,
	"ascii_uppercase" : lambda: string.ascii_uppercase,
	"digits" : lambda: string.digits,
	"hexdigits" : lambda: string.hexdigits,
	"letters" : lambda: string.letters,
	"lowercase" : lambda: string.lowercase,
	"octdigits" : lambda: string.octdigits,
	"punctuation" : lambda: string.punctuation,
	"printable" : lambda: string.printable,
	"uppercase" : lambda: string.uppercase,
	"whitespace" : lambda: string.whitespace
}