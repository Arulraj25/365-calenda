from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from collections import defaultdict
import random

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# In-memory storage
views_data = defaultdict(int)

# Your complete 365 days data
special_days = [
  {"date":"01-01","day":"New Year's Day","description":"The first day of the year"},
  {"date":"01-02","day":"Science Fiction Day","description":"Celebrate science fiction"},
  {"date":"01-03","day":"Festival of Sleep Day","description":"Time to catch up on sleep"},
  {"date":"01-04","day":"World Braille Day","description":"Raise awareness about Braille literacy"},
  {"date":"01-05","day":"National Bird Day","description":"Celebrate birds and their conservation"},
  {"date":"01-06","day":"Epiphany / Three Kings' Day","description":"Christian feast day"},
  {"date":"01-07","day":"Orthodox Christmas","description":"Christmas celebration by Orthodox Christians"},
  {"date":"01-08","day":"Bubble Bath Day","description":"Relax in a bubble bath"},
  {"date":"01-09","day":"National Law Enforcement Appreciation Day","description":"Honor law enforcement officers"},
  {"date":"01-10","day":"Houseplant Appreciation Day","description":"Celebrate indoor plants"},
  {"date":"01-11","day":"International Thank-You Day","description":"Show gratitude to others"},
  {"date":"01-12","day":"National Pharmacist Day","description":"Recognize pharmacists"},
  {"date":"01-13","day":"National Rubber Ducky Day","description":"Celebrate the classic bath toy"},
  {"date":"01-14","day":"National Dress Up Your Pet Day","description":"Dress your pet in fun outfits"},
  {"date":"01-15","day":"Martin Luther King Jr. Day","description":"Honor civil rights leader (3rd Monday in January, USA)"},
  {"date":"01-16","day":"Appreciate a Dragon Day","description":"Celebrate dragons in stories and imagination"},
  {"date":"01-17","day":"Kid Inventors' Day","description":"Celebrate young inventors"},
  {"date":"01-18","day":"Winnie the Pooh Day","description":"Honoring A.A. Milne's beloved character"},
  {"date":"01-19","day":"Popcorn Day","description":"Celebrate the tasty snack"},
  {"date":"01-20","day":"Penguin Awareness Day","description":"Raise awareness about penguins"},
  {"date":"01-21","day":"Squirrel Appreciation Day","description":"Celebrate squirrels"},
  {"date":"01-22","day":"National Blonde Brownie Day","description":"Enjoy this sweet treat"},
  {"date":"01-23","day":"National Pie Day","description":"Celebrate pies of all kinds"},
  {"date":"01-24","day":"Compliment Day","description":"Give someone a compliment"},
  {"date":"01-25","day":"Opposite Day","description":"Do things the opposite way"},
  {"date":"01-26","day":"Republic Day (India)","description":"National holiday in India"},
  {"date":"01-27","day":"International Holocaust Remembrance Day","description":"Remember the victims of the Holocaust"},
  {"date":"01-28","day":"Data Privacy Day","description":"Promote awareness of data protection"},
  {"date":"01-29","day":"Puzzle Day","description":"Challenge yourself with puzzles"},
  {"date":"01-30","day":"Martyrs' Day (India)","description":"Honoring martyrs in India"},
  {"date":"01-31","day":"Inspire Your Heart With Art Day","description":"Enjoy and create art"},
  
  {"date":"02-01","day":"World Hijab Day","description":"Promote understanding about the hijab"},
  {"date":"02-02","day":"Groundhog Day","description":"Predict the coming of spring"},
  {"date":"02-03","day":"National Women Physicians Day","description":"Celebrate female doctors"},
  {"date":"02-04","day":"World Cancer Day","description":"Raise awareness for cancer"},
  {"date":"02-05","day":"World Nutella Day","description":"Celebrate the beloved hazelnut spread"},
  {"date":"02-06","day":"Lame Duck Day","description":"Mark the end of political terms"},
  {"date":"02-07","day":"Send a Card to a Friend Day","description":"Send a card to a friend"},
  {"date":"02-08","day":"Kite Flying Day","description":"Enjoy flying kites"},
  {"date":"02-09","day":"National Pizza Day","description":"Celebrate pizza lovers"},
  {"date":"02-10","day":"Umbrella Day","description":"Appreciate the humble umbrella"},
  {"date":"02-11","day":"International Day of Women and Girls in Science","description":"Promote women in science"},
  {"date":"02-12","day":"Darwin Day","description":"Celebrate Charles Darwin"},
  {"date":"02-13","day":"Galentine's Day","description":"Celebrate friendship among women"},
  {"date":"02-14","day":"Valentine's Day","description":"Day of love and affection"},
  {"date":"02-15","day":"Singles Awareness Day","description":"Celebrate being single"},
  {"date":"02-16","day":"Do a Grouch a Favor Day","description":"Do something nice for a grouch"},
  {"date":"02-17","day":"Random Acts of Kindness Day","description":"Perform random acts of kindness"},
  {"date":"02-18","day":"Battery Day","description":"Celebrate the invention of batteries"},
  {"date":"02-19","day":"Chocolate Mint Day","description":"Enjoy chocolate mint treats"},
  {"date":"02-20","day":"Love Your Pet Day","description":"Show love to your pets"},
  {"date":"02-21","day":"International Mother Language Day","description":"Promote linguistic diversity"},
  {"date":"02-22","day":"World Thinking Day","description":"Think globally, act locally"},
  {"date":"02-23","day":"Dog Biscuit Day","description":"Treat your dog with biscuits"},
  {"date":"02-24","day":"Tortilla Chip Day","description":"Enjoy tortilla chips"},
  {"date":"02-25","day":"Clam Chowder Day","description":"Celebrate clam chowder"},
  {"date":"02-26","day":"Tell a Fairy Tale Day","description":"Share a fairy tale"},
  {"date":"02-27","day":"No Brainer Day","description":"Do something simple today"},
  {"date":"02-28","day":"National Science Day (India)","description":"Celebrate science achievements in India"},
  {"date":"02-29","day":"Leap Day","description":"Occurs only every 4 years"},
  
  {"date":"03-01","day":"Zero Discrimination Day","description":"Promote equality and inclusion"},
  {"date":"03-02","day":"Old Stuff Day","description":"Celebrate vintage and old items"},
  {"date":"03-03","day":"World Wildlife Day","description":"Raise awareness for wildlife conservation"},
  {"date":"03-04","day":"National Grammar Day","description":"Celebrate proper grammar"},
  {"date":"03-05","day":"Cheese Doodle Day","description":"Enjoy cheesy snacks"},
  {"date":"03-06","day":"Dentist's Day","description":"Appreciate dentists"},
  {"date":"03-07","day":"Be Heard Day","description":"Encourage people to speak up"},
  {"date":"03-08","day":"International Women's Day","description":"Celebrate women's achievements"},
  {"date":"03-09","day":"Meatball Day","description":"Enjoy meatballs"},
  {"date":"03-10","day":"Pack Your Lunch Day","description":"Bring lunch from home"},
  {"date":"03-11","day":"World Plumbing Day","description":"Recognize plumbing professionals"},
  {"date":"03-12","day":"Plant a Flower Day","description":"Plant flowers and beautify your space"},
  {"date":"03-13","day":"Ear Muff Day","description":"Keep warm with earmuffs"},
  {"date":"03-14","day":"Pi Day","description":"Celebrate the mathematical constant π"},
  {"date":"03-15","day":"World Consumer Rights Day","description":"Promote consumer rights"},
  {"date":"03-16","day":"Everything You Do is Right Day","description":"Boost self-confidence"},
  {"date":"03-17","day":"St. Patrick's Day","description":"Celebrate Irish culture"},
  {"date":"03-18","day":"Awkward Moments Day","description":"Laugh at awkward situations"},
  {"date":"03-19","day":"Let's Laugh Day","description":"Encourage laughter and joy"},
  {"date":"03-20","day":"International Day of Happiness","description":"Promote happiness worldwide"},
  {"date":"03-21","day":"World Poetry Day / Forest Day / Down Syndrome Day","description":"Celebrate poetry, forests, and Down Syndrome awareness"},
  {"date":"03-22","day":"World Water Day","description":"Raise awareness about freshwater"},
  {"date":"03-23","day":"Meteorological Day","description":"Recognize meteorology"},
  {"date":"03-24","day":"World Tuberculosis Day","description":"Raise awareness for TB"},
  {"date":"03-25","day":"Tolkien Reading Day","description":"Celebrate J.R.R. Tolkien"},
  {"date":"03-26","day":"Spinach Day","description":"Enjoy healthy spinach"},
  {"date":"03-27","day":"World Theatre Day","description":"Celebrate theater arts"},
  {"date":"03-28","day":"Respect Your Cat Day","description":"Show respect to cats"},
  {"date":"03-29","day":"Mom and Pop Business Owners Day","description":"Support small businesses"},
  {"date":"03-30","day":"Doctors' Day","description":"Appreciate doctors"},
  {"date":"03-31","day":"Crayon Day","description":"Celebrate crayons and coloring"},

  {"date":"04-01","day":"April Fools' Day","description":"Day for harmless pranks"},
  {"date":"04-02","day":"World Autism Awareness Day","description":"Raise awareness about autism"},
  {"date":"04-03","day":"Find a Rainbow Day","description":"Celebrate rainbows and colors"},
  {"date":"04-04","day":"International Carrot Day","description":"Appreciate carrots and healthy eating"},
  {"date":"04-05","day":"Read a Road Map Day","description":"Practice map reading skills"},
  {"date":"04-06","day":"Student Athlete Day","description":"Celebrate student athletes"},
  {"date":"04-07","day":"World Health Day","description":"Promote health awareness"},
  {"date":"04-08","day":"Draw a Picture of a Bird Day","description":"Draw and appreciate birds"},
  {"date":"04-09","day":"Name Yourself Day","description":"Choose your own name for a day"},
  {"date":"04-10","day":"Siblings Day","description":"Celebrate brothers and sisters"},
  {"date":"04-11","day":"Submarine Day","description":"Celebrate submarines and naval history"},
  {"date":"04-12","day":"International Day of Human Space Flight","description":"Celebrate space exploration"},
  {"date":"04-13","day":"Scrabble Day / Baisakhi","description":"Play Scrabble or celebrate Baisakhi"},
  {"date":"04-14","day":"Look Up at the Sky Day","description":"Spend time looking at the sky"},
  {"date":"04-15","day":"Titanic Remembrance Day","description":"Remember the Titanic disaster"},
  {"date":"04-16","day":"Save the Elephant Day","description":"Raise awareness about elephant conservation"},
  {"date":"04-17","day":"Bat Appreciation Day","description":"Celebrate bats and their ecological role"},
  {"date":"04-18","day":"Animal Crackers Day","description":"Enjoy animal-shaped crackers"},
  {"date":"04-19","day":"Bicycle Day","description":"Celebrate bicycles and cycling"},
  {"date":"04-20","day":"Volunteer Recognition Day","description":"Recognize volunteers"},
  {"date":"04-21","day":"Kindergarten Day","description":"Celebrate kindergarten teachers and students"},
  {"date":"04-22","day":"Earth Day","description":"Protect our planet"},
  {"date":"04-23","day":"World Book Day","description":"Promote reading and literacy"},
  {"date":"04-24","day":"Pigs in a Blanket Day","description":"Enjoy this fun snack"},
  {"date":"04-25","day":"DNA Day","description":"Celebrate genetics and DNA discoveries"},
  {"date":"04-26","day":"Hug an Australian Day","description":"Send hugs to Australians"},
  {"date":"04-27","day":"Morse Code Day","description":"Celebrate the invention of Morse code"},
  {"date":"04-28","day":"Superhero Day","description":"Celebrate superheroes"},
  {"date":"04-29","day":"International Dance Day","description":"Celebrate dance in all forms"},
  {"date":"04-30","day":"International Jazz Day","description":"Celebrate jazz music"},

  {"date":"05-01","day":"International Workers' Day","description":"Celebrate workers and labor rights"},
  {"date":"05-02","day":"World Tuna Day","description":"Raise awareness about tuna conservation"},
  {"date":"05-03","day":"World Press Freedom Day","description":"Promote press freedom worldwide"},
  {"date":"05-04","day":"Star Wars Day","description":"May the Fourth be with you"},
  {"date":"05-05","day":"Cinco de Mayo","description":"Celebrate Mexican heritage"},
  {"date":"05-06","day":"No Diet Day","description":"Take a break from dieting"},
  {"date":"05-07","day":"National Tourism Day","description":"Promote tourism"},
  {"date":"05-08","day":"World Red Cross Day","description":"Celebrate humanitarian work"},
  {"date":"05-09","day":"Europe Day","description":"Celebrate peace and unity in Europe"},
  {"date":"05-10","day":"Mother's Day","description":"Honor mothers"},
  {"date":"05-11","day":"Twilight Zone Day","description":"Celebrate the classic TV show"},
  {"date":"05-12","day":"International Nurses Day","description":"Recognize nurses' contributions"},
  {"date":"05-13","day":"Frog Jumping Day","description":"Celebrate frogs and fun activities"},
  {"date":"05-14","day":"Buddha Purnima","description":"Celebrate Buddha's birth and enlightenment"},
  {"date":"05-15","day":"International Day of Families","description":"Celebrate family life"},
  {"date":"05-16","day":"Love a Tree Day","description":"Appreciate and care for trees"},
  {"date":"05-17","day":"World Telecommunication Day","description":"Celebrate telecommunications"},
  {"date":"05-18","day":"Museum Day","description":"Visit and appreciate museums"},
  {"date":"05-19","day":"World Plant a Vegetable Day","description":"Encourage vegetable gardening"},
  {"date":"05-20","day":"Be a Millionaire Day","description":"Have fun imagining being a millionaire"},
  {"date":"05-21","day":"World Day for Cultural Diversity","description":"Celebrate cultural diversity"},
  {"date":"05-22","day":"International Day for Biological Diversity","description":"Raise awareness about biodiversity"},
  {"date":"05-23","day":"World Turtle Day","description":"Celebrate turtles and their protection"},
  {"date":"05-24","day":"Brother's Day","description":"Honor brothers"},
  {"date":"05-25","day":"Geek Pride Day","description":"Celebrate geek culture"},
  {"date":"05-26","day":"Sally Ride Day","description":"Honor astronaut Sally Ride"},
  {"date":"05-27","day":"Sunscreen Day","description":"Promote sun safety"},
  {"date":"05-28","day":"Hamburger Day","description":"Enjoy hamburgers"},
  {"date":"05-29","day":"International Day of UN Peacekeepers","description":"Honor UN peacekeepers"},
  {"date":"05-30","day":"Water a Flower Day","description":"Care for flowers"},
  {"date":"05-31","day":"Anti-Tobacco Day","description":"Raise awareness about tobacco dangers"},

  {"date":"06-01","day":"Global Day of Parents","description":"Celebrate parents worldwide"},
  {"date":"06-02","day":"International Sex Workers' Day","description":"Raise awareness about sex workers' rights"},
  {"date":"06-03","day":"World Bicycle Day","description":"Celebrate bicycles and cycling"},
  {"date":"06-04","day":"Hug Your Cat Day","description":"Show affection to your cat"},
  {"date":"06-05","day":"World Environment Day","description":"Promote environmental protection"},
  {"date":"06-06","day":"National Gardening Exercise Day","description":"Exercise while gardening"},
  {"date":"06-07","day":"Chocolate Ice Cream Day","description":"Enjoy chocolate ice cream"},
  {"date":"06-08","day":"Best Friends Day","description":"Celebrate friendship"},
  {"date":"06-09","day":"Donald Duck Day","description":"Celebrate the cartoon character"},
  {"date":"06-10","day":"Ballpoint Pen Day","description":"Celebrate the invention of the pen"},
  {"date":"06-11","day":"Corn on the Cob Day","description":"Enjoy corn on the cob"},
  {"date":"06-12","day":"World Day Against Child Labour","description":"Raise awareness about child labor"},
  {"date":"06-13","day":"Sewing Machine Day","description":"Celebrate the sewing machine invention"},
  {"date":"06-14","day":"World Blood Donor Day","description":"Encourage blood donation"},
  {"date":"06-15","day":"Nature Photography Day / Father's Day","description":"Celebrate nature photography and fathers (3rd Sunday of June)"},
  {"date":"06-16","day":"Fresh Veggies Day","description":"Eat fresh vegetables"},
  {"date":"06-17","day":"Eat Your Vegetables Day","description":"Encourage healthy eating"},
  {"date":"06-18","day":"International Picnic Day","description":"Enjoy a picnic outdoors"},
  {"date":"06-19","day":"World Sickle Cell Day / Juneteenth","description":"Raise awareness about sickle cell and celebrate freedom (USA)"},
  {"date":"06-20","day":"World Refugee Day","description":"Support refugees worldwide"},
  {"date":"06-21","day":"International Yoga Day / Summer Solstice","description":"Practice yoga and celebrate the solstice"},
  {"date":"06-22","day":"Onion Ring Day","description":"Enjoy onion rings"},
  {"date":"06-23","day":"Typewriter Day","description":"Celebrate the invention of the typewriter"},
  {"date":"06-24","day":"Swim a Lap Day","description":"Go swimming"},
  {"date":"06-25","day":"Take Your Dog to Work Day","description":"Bring your dog to work"},
  {"date":"06-26","day":"International Day Against Drug Abuse","description":"Raise awareness against drug abuse"},
  {"date":"06-27","day":"Sunglasses Day","description":"Wear your sunglasses"},
  {"date":"06-28","day":"Paul Bunyan Day","description":"Celebrate the legendary lumberjack"},
  {"date":"06-29","day":"Camera Day","description":"Celebrate photography"},
  {"date":"06-30","day":"Social Media Day","description":"Recognize social media's impact"},

  {"date":"07-01","day":"Doctor's Day","description":"Celebrate doctors and their contributions"},
  {"date":"07-02","day":"I Forgot Day","description":"For those forgetful moments"},
  {"date":"07-03","day":"Stay Out of the Sun Day","description":"Avoid sun exposure"},
  {"date":"07-04","day":"Independence Day","description":"American independence celebration"},
  {"date":"07-05","day":"Workaholics Day","description":"Celebrate hardworking people"},
  {"date":"07-06","day":"International Kissing Day","description":"Celebrate kisses"},
  {"date":"07-07","day":"World Chocolate Day","description":"Enjoy chocolate treats"},
  {"date":"07-08","day":"Video Games Day","description":"Celebrate video gaming"},
  {"date":"07-09","day":"Sugar Cookie Day","description":"Enjoy sugar cookies"},
  {"date":"07-10","day":"Don't Step on a Bee Day","description":"Protect bees and their habitats"},
  {"date":"07-11","day":"World Population Day","description":"Raise awareness about population issues"},
  {"date":"07-12","day":"Simplicity Day","description":"Celebrate simple living"},
  {"date":"07-13","day":"Embrace Your Geekness Day","description":"Celebrate geek culture"},
  {"date":"07-14","day":"Bastille Day","description":"French national holiday"},
  {"date":"07-15","day":"Gummi Worm Day","description":"Enjoy gummy worms"},
  {"date":"07-16","day":"World Snake Day","description":"Celebrate snakes and their role in nature"},
  {"date":"07-17","day":"World Emoji Day","description":"Celebrate emojis"},
  {"date":"07-18","day":"Nelson Mandela International Day","description":"Honor Nelson Mandela's legacy"},
  {"date":"07-19","day":"National Daiquiri Day","description":"Celebrate the daiquiri cocktail"},
  {"date":"07-20","day":"Moon Day / Space Exploration Day","description":"Celebrate space exploration"},
  {"date":"07-21","day":"Junk Food Day","description":"Enjoy indulgent treats"},
  {"date":"07-22","day":"Hammock Day","description":"Relax in a hammock"},
  {"date":"07-23","day":"Gorgeous Grandma Day","description":"Celebrate grandmothers"},
  {"date":"07-24","day":"Cousins Day","description":"Celebrate cousins"},
  {"date":"07-25","day":"Threading the Needle Day","description":"Practice precision and skill"},
  {"date":"07-26","day":"Aunt and Uncle Day","description":"Celebrate aunts and uncles"},
  {"date":"07-27","day":"Take Your Pants for a Walk Day","description":"A fun, silly day"},
  {"date":"07-28","day":"World Hepatitis Day","description":"Raise awareness about hepatitis"},
  {"date":"07-29","day":"Lipstick Day","description":"Celebrate wearing lipstick"},
  {"date":"07-30","day":"International Day of Friendship","description":"Celebrate friendships worldwide"},
  {"date":"07-31","day":"Avocado Day","description":"Enjoy avocados"},

  {"date":"08-01","day":"National Girlfriends Day","description":"Celebrate girlfriends"},
  {"date":"08-02","day":"Ice Cream Sandwich Day","description":"Enjoy ice cream sandwiches"},
  {"date":"08-03","day":"Watermelon Day / International Friendship Day","description":"Celebrate watermelons and friendship"},
  {"date":"08-04","day":"Coast Guard Day","description":"Honor the Coast Guard"},
  {"date":"08-05","day":"National Oyster Day","description":"Celebrate oysters"},
  {"date":"08-06","day":"Hiroshima Day","description":"Remember the Hiroshima bombing"},
  {"date":"08-07","day":"Lighthouse Day","description":"Celebrate lighthouses"},
  {"date":"08-08","day":"International Cat Day","description":"Celebrate cats"},
  {"date":"08-09","day":"Quit India Day / Nagasaki Day","description":"Remember historical events"},
  {"date":"08-10","day":"Lazy Day","description":"Take a break and relax"},
  {"date":"08-11","day":"Son and Daughter Day","description":"Celebrate children"},
  {"date":"08-12","day":"International Youth Day","description":"Celebrate youth contributions"},
  {"date":"08-13","day":"Left-Handers Day","description":"Celebrate left-handed people"},
  {"date":"08-14","day":"National Creamsicle Day","description":"Enjoy creamsicles"},
  {"date":"08-15","day":"Independence Day (India)","description":"Indian national holiday"},
  {"date":"08-16","day":"National Rum Day","description":"Celebrate rum"},
  {"date":"08-17","day":"National Thrift Shop Day","description":"Celebrate thrifting and second-hand shopping"},
  {"date":"08-18","day":"Bad Poetry Day","description":"Celebrate intentionally bad poetry"},
  {"date":"08-19","day":"World Photography Day","description":"Celebrate photography"},
  {"date":"08-20","day":"Senior Citizens Day","description":"Honor senior citizens"},
  {"date":"08-21","day":"Spumoni Day","description":"Enjoy spumoni ice cream"},
  {"date":"08-22","day":"National Tooth Fairy Day","description":"Celebrate the tooth fairy tradition"},
  {"date":"08-23","day":"Ride the Wind Day","description":"Enjoy outdoor activities"},
  {"date":"08-24","day":"World Humanitarian Day","description":"Honor humanitarian efforts"},
  {"date":"08-25","day":"Kiss and Make Up Day","description":"Make peace with someone"},
  {"date":"08-26","day":"Women's Equality Day","description":"Celebrate gender equality"},
  {"date":"08-27","day":"Just Because Day","description":"Do something just because"},
  {"date":"08-28","day":"Raksha Bandhan","description":"Celebrate sibling bonds (2026)"},
  {"date":"08-29","day":"National Sports Day (India)","description":"Promote sports activities in India"},
  {"date":"08-30","day":"Frankenstein Day","description":"Celebrate Mary Shelley's Frankenstein"},
  {"date":"08-31","day":"Eat Outside Day","description":"Enjoy outdoor meals"},

  {"date":"09-01","day":"Letter Writing Day","description":"Celebrate letter writing"},
  {"date":"09-02","day":"V-J Day / Coconut Day","description":"Remember V-J Day and enjoy coconuts"},
  {"date":"09-03","day":"Skyscraper Day","description":"Celebrate skyscrapers"},
  {"date":"09-04","day":"Newspaper Carrier Day","description":"Appreciate newspaper carriers"},
  {"date":"09-05","day":"Teachers' Day (India)","description":"Celebrate teachers in India"},
  {"date":"09-06","day":"Fight Procrastination Day","description":"Encourage productivity"},
  {"date":"09-07","day":"National Salami Day","description":"Celebrate salami"},
  {"date":"09-08","day":"International Literacy Day","description":"Promote literacy worldwide"},
  {"date":"09-09","day":"Teddy Bear Day","description":"Celebrate teddy bears"},
  {"date":"09-10","day":"Swap Ideas Day","description":"Exchange ideas and thoughts"},
  {"date":"09-11","day":"Make Your Bed Day","description":"Practice making your bed"},
  {"date":"09-12","day":"Chocolate Milkshake Day","description":"Enjoy chocolate milkshakes"},
  {"date":"09-13","day":"Programmers' Day","description":"Celebrate programmers (256th day of the year)"},
  {"date":"09-14","day":"National Cream-Filled Donut Day","description":"Enjoy cream-filled donuts"},
  {"date":"09-15","day":"International Dot Day","description":"Celebrate creativity and dots"},
  {"date":"09-16","day":"World Ozone Day","description":"Raise awareness about the ozone layer"},
  {"date":"09-17","day":"Constitution Day (USA)","description":"Celebrate the U.S. Constitution"},
  {"date":"09-18","day":"Respect for the Aged Day","description":"Honor senior citizens"},
  {"date":"09-19","day":"Talk Like a Pirate Day","description":"Have fun speaking like a pirate"},
  {"date":"09-20","day":"Pepperoni Pizza Day","description":"Enjoy pepperoni pizza"},
  {"date":"09-21","day":"International Day of Peace","description":"Promote world peace"},
  {"date":"09-22","day":"Hobbit Day / Elephant Appreciation Day","description":"Celebrate Hobbits and elephants"},
  {"date":"09-23","day":"Checkers Day / Autumnal Equinox","description":"Celebrate checkers or the fall equinox"},
  {"date":"09-24","day":"Punctuation Day","description":"Celebrate proper punctuation"},
  {"date":"09-25","day":"Daughters Day","description":"Honor daughters"},
  {"date":"09-26","day":"European Day of Languages","description":"Celebrate linguistic diversity"},
  {"date":"09-27","day":"World Tourism Day","description":"Promote tourism worldwide"},
  {"date":"09-28","day":"Ask a Stupid Question Day","description":"Encourage curiosity"},
  {"date":"09-29","day":"World Heart Day","description":"Promote heart health"},
  {"date":"09-30","day":"Hot Mulled Cider Day","description":"Enjoy warm mulled cider"},

  {"date":"10-01","day":"International Coffee Day","description":"Celebrate coffee lovers around the world"},
  {"date":"10-02","day":"Gandhi Jayanti / International Day of Non-Violence","description":"Honor Gandhi and promote non-violence"},
  {"date":"10-03","day":"World Habitat Day","description":"Raise awareness about human settlements"},
  {"date":"10-04","day":"World Animal Day","description":"Celebrate animals and promote their welfare"},
  {"date":"10-05","day":"World Teachers' Day","description":"Honor teachers worldwide"},
  {"date":"10-06","day":"Mad Hatter Day","description":"Celebrate quirky hats and fun"},
  {"date":"10-07","day":"World Smile Day","description":"Encourage smiling and kindness"},
  {"date":"10-08","day":"Do Something Nice Day","description":"Perform a random act of kindness"},
  {"date":"10-09","day":"World Post Day","description":"Celebrate postal services"},
  {"date":"10-10","day":"World Mental Health Day","description":"Raise awareness about mental health"},
  {"date":"10-11","day":"National Coming Out Day","description":"Support the LGBTQ+ community"},
  {"date":"10-12","day":"Farmer's Day / Columbus Day","description":"Celebrate farmers or Columbus Day (varies)"},
  {"date":"10-13","day":"International Skeptics Day","description":"Celebrate critical thinking"},
  {"date":"10-14","day":"Be Bald and Be Free Day","description":"Embrace baldness and confidence"},
  {"date":"10-15","day":"Global Handwashing Day","description":"Promote hand hygiene"},
  {"date":"10-16","day":"World Food Day","description":"Raise awareness about food security"},
  {"date":"10-17","day":"Black Poetry Day","description":"Celebrate African-American poetry"},
  {"date":"10-18","day":"Chocolate Cupcake Day","description":"Enjoy chocolate cupcakes"},
  {"date":"10-19","day":"Evaluate Your Life Day","description":"Reflect on life choices"},
  {"date":"10-20","day":"World Statistics Day","description":"Highlight the importance of statistics"},
  {"date":"10-21","day":"Reptile Awareness Day","description":"Raise awareness about reptiles"},
  {"date":"10-22","day":"Caps Lock Day","description":"Have fun with CAPS LOCK"},
  {"date":"10-23","day":"Mole Day","description":"Celebrate the chemistry concept of a mole"},
  {"date":"10-24","day":"United Nations Day","description":"Celebrate the founding of the UN"},
  {"date":"10-25","day":"World Pasta Day","description":"Celebrate pasta lovers"},
  {"date":"10-26","day":"National Pumpkin Day","description":"Enjoy pumpkins"},
  {"date":"10-27","day":"American Beer Day","description":"Celebrate American beer"},
  {"date":"10-28","day":"National Chocolate Day","description":"Enjoy chocolate treats"},
  {"date":"10-29","day":"Internet Day","description":"Celebrate the invention of the internet"},
  {"date":"10-30","day":"Mischief Night","description":"Night of harmless pranks"},
  {"date":"10-31","day":"Halloween / World Cities Day","description":"Spooky fun and urban awareness"},

  {"date":"11-01","day":"World Vegan Day","description":"Celebrate vegan lifestyle"},
  {"date":"11-02","day":"All Souls' Day","description":"Remember deceased loved ones"},
  {"date":"11-03","day":"Sandwich Day","description":"Enjoy sandwiches"},
  {"date":"11-04","day":"King Tut Day","description":"Celebrate King Tutankhamun"},
  {"date":"11-05","day":"Guy Fawkes Day","description":"Commemorate Guy Fawkes"},
  {"date":"11-06","day":"Saxophone Day","description":"Celebrate the saxophone"},
  {"date":"11-07","day":"National Cancer Awareness Day","description":"Raise awareness about cancer"},
  {"date":"11-08","day":"Cook Something Bold Day","description":"Try bold new recipes"},
  {"date":"11-09","day":"Legal Services Day","description":"Appreciate legal professionals"},
  {"date":"11-10","day":"World Science Day for Peace & Development","description":"Promote science for society"},
  {"date":"11-11","day":"Veterans Day / Remembrance Day","description":"Honor veterans worldwide"},
  {"date":"11-12","day":"Happy Hour Day","description":"Celebrate relaxing with drinks"},
  {"date":"11-13","day":"World Kindness Day","description":"Encourage acts of kindness"},
  {"date":"11-14","day":"World Diabetes Day / Children's Day (India)","description":"Raise awareness about diabetes"},
  {"date":"11-15","day":"America Recycles Day","description":"Promote recycling efforts"},
  {"date":"11-16","day":"International Day for Tolerance","description":"Promote tolerance and understanding"},
  {"date":"11-17","day":"Students' Day","description":"Celebrate students"},
  {"date":"11-18","day":"Mickey Mouse Day","description":"Celebrate Mickey Mouse"},
  {"date":"11-19","day":"International Men's Day","description":"Celebrate men's contributions"},
  {"date":"11-20","day":"Universal Children's Day","description":"Promote children's rights"},
  {"date":"11-21","day":"World Television Day","description":"Celebrate television"},
  {"date":"11-22","day":"Go For a Ride Day","description":"Enjoy a fun ride"},
  {"date":"11-23","day":"Fibonacci Day","description":"Celebrate the Fibonacci sequence (11/23)"},
  {"date":"11-24","day":"Celebrate Your Unique Talent Day","description":"Show off your talents"},
  {"date":"11-25","day":"International Day for the Elimination of Violence Against Women","description":"Raise awareness and prevent violence against women"},
  {"date":"11-26","day":"Thanksgiving (USA)","description":"American holiday for gratitude (4th Thursday)"},
  {"date":"11-27","day":"Pins and Needles Day","description":"Recognize the feeling of anticipation"},
  {"date":"11-28","day":"Red Planet Day","description":"Celebrate Mars exploration"},
  {"date":"11-29","day":"Electronic Greeting Card Day","description":"Send e-cards to loved ones"},
  {"date":"11-30","day":"Stay at Home Because You're Well Day","description":"Take a personal health day"},

  {"date":"12-01","day":"World AIDS Day","description":"Raise awareness about HIV/AIDS"},
  {"date":"12-02","day":"International Day for the Abolition of Slavery / Computer Literacy Day","description":"Promote human rights and digital literacy"},
  {"date":"12-03","day":"International Day of Persons with Disabilities","description":"Celebrate and support persons with disabilities"},
  {"date":"12-04","day":"Indian Navy Day","description":"Honor the Indian Navy"},
  {"date":"12-05","day":"Volunteer Day / International Ninja Day","description":"Celebrate volunteering and ninjas"},
  {"date":"12-06","day":"Saint Nicholas Day","description":"Celebrate Saint Nicholas"},
  {"date":"12-07","day":"Pearl Harbor Remembrance Day / Armed Forces Flag Day (India)","description":"Remember Pearl Harbor and honor armed forces"},
  {"date":"12-08","day":"Pretend to Be a Time Traveler Day","description":"Have fun pretending to time travel"},
  {"date":"12-09","day":"Christmas Card Day","description":"Send Christmas cards"},
  {"date":"12-10","day":"Human Rights Day","description":"Promote human rights globally"},
  {"date":"12-11","day":"International Mountain Day","description":"Celebrate mountains and hiking"},
  {"date":"12-12","day":"Poinsettia Day","description":"Enjoy poinsettias"},
  {"date":"12-13","day":"National Cocoa Day","description":"Drink hot cocoa"},
  {"date":"12-14","day":"Monkey Day","description":"Celebrate monkeys"},
  {"date":"12-15","day":"Bill of Rights Day","description":"Celebrate the U.S. Bill of Rights"},
  {"date":"12-16","day":"Day of Reconciliation (South Africa)","description":"Promote reconciliation in South Africa"},
  {"date":"12-17","day":"Wright Brothers Day","description":"Honor the Wright brothers' achievements"},
  {"date":"12-18","day":"Bake Cookies Day","description":"Bake and enjoy cookies"},
  {"date":"12-19","day":"Oatmeal Muffin Day","description":"Enjoy oatmeal muffins"},
  {"date":"12-20","day":"International Human Solidarity Day","description":"Promote solidarity and unity"},
  {"date":"12-21","day":"Crossword Puzzle Day / Winter Solstice","description":"Enjoy crosswords and celebrate the winter solstice"},
  {"date":"12-22","day":"National Mathematics Day (India)","description":"Celebrate mathematics in India"},
  {"date":"12-23","day":"Farmers' Day / Kisan Diwas (India)","description":"Honor farmers in India"},
  {"date":"12-24","day":"National Eggnog Day / Christmas Eve","description":"Enjoy eggnog and prepare for Christmas"},
  {"date":"12-25","day":"Christmas Day","description":"Celebrate Christmas"},
  {"date":"12-26","day":"Boxing Day","description":"Holiday following Christmas"},
  {"date":"12-27","day":"Make Cut-Out Snowflakes Day","description":"Create paper snowflakes"},
  {"date":"12-28","day":"Card Playing Day","description":"Play card games"},
  {"date":"12-29","day":"Pepper Pot Day","description":"Enjoy pepper pot stew"},
  {"date":"12-30","day":"Bacon Day","description":"Celebrate bacon lovers"},
  {"date":"12-31","day":"New Year's Eve","description":"Ring in the new year"}
]

def enrich_data():
    """Add metadata to each day"""
    for day in special_days:
        if 'icon' not in day:
            day['icon'] = get_icon(day['day'])
        if 'color' not in day:
            day['color'] = get_color(day['day'])
        if 'animation' not in day:
            day['animation'] = get_animation(day['day'])
        if 'category' not in day:
            day['category'] = get_category(day['day'])

def get_icon(day_name):
    """Get icon for day"""
    lower = day_name.lower()
    if 'new year' in lower or 'eve' in lower:
        return 'fas fa-glass-cheers'
    elif 'science' in lower or 'math' in lower or 'pi' in lower or 'fibonacci' in lower:
        return 'fas fa-flask'
    elif 'sleep' in lower or 'bed' in lower:
        return 'fas fa-bed'
    elif 'bird' in lower or 'penguin' in lower or 'squirrel' in lower or 'dragon' in lower or 'elephant' in lower or 'bat' in lower or 'turtle' in lower or 'snake' in lower or 'cat' in lower or 'dog' in lower or 'pet' in lower or 'animal' in lower or 'wildlife' in lower or 'monkey' in lower:
        return 'fas fa-paw'
    elif 'valentine' in lower or 'love' in lower or 'heart' in lower:
        return 'fas fa-heart'
    elif 'food' in lower or 'pizza' in lower or 'chocolate' in lower or 'ice cream' in lower or 'burger' in lower or 'pasta' in lower or 'cookie' in lower or 'cake' in lower or 'pie' in lower or 'nutella' in lower or 'popcorn' in lower or 'brownie' in lower or 'cheese' in lower or 'salami' in lower or 'donut' in lower or 'bacon' in lower or 'avocado' in lower or 'watermelon' in lower or 'coconut' in lower or 'corn' in lower or 'carrot' in lower or 'pumpkin' in lower:
        return 'fas fa-utensils'
    elif 'coffee' in lower or 'tea' in lower or 'drink' in lower or 'beer' in lower or 'daiquiri' in lower or 'rum' in lower or 'cider' in lower:
        return 'fas fa-mug-hot'
    elif 'space' in lower or 'moon' in lower or 'planet' in lower or 'rocket' in lower:
        return 'fas fa-rocket'
    elif 'art' in lower or 'paint' in lower or 'draw' in lower or 'crayon' in lower:
        return 'fas fa-palette'
    elif 'music' in lower or 'dance' in lower or 'jazz' in lower or 'saxophone' in lower:
        return 'fas fa-music'
    elif 'book' in lower or 'reading' in lower or 'literacy' in lower or 'poetry' in lower:
        return 'fas fa-book'
    elif 'film' in lower or 'movie' in lower or 'video' in lower or 'television' in lower:
        return 'fas fa-film'
    elif 'photo' in lower or 'camera' in lower:
        return 'fas fa-camera'
    elif 'computer' in lower or 'internet' in lower or 'programmer' in lower or 'tech' in lower:
        return 'fas fa-laptop'
    elif 'tree' in lower or 'plant' in lower or 'flower' in lower or 'garden' in lower:
        return 'fas fa-seedling'
    elif 'christmas' in lower:
        return 'fas fa-tree'
    elif 'halloween' in lower:
        return 'fas fa-ghost'
    elif 'thanksgiving' in lower:
        return 'fas fa-drumstick-bite'
    elif 'easter' in lower:
        return 'fas fa-egg'
    elif 'st. patrick' in lower:
        return 'fas fa-clover'
    elif 'peace' in lower or 'dove' in lower:
        return 'fas fa-peace'
    elif 'health' in lower or 'doctor' in lower or 'nurse' in lower or 'dentist' in lower:
        return 'fas fa-heartbeat'
    elif 'education' in lower or 'teacher' in lower or 'student' in lower:
        return 'fas fa-graduation-cap'
    elif 'family' in lower or 'mother' in lower or 'father' in lower or 'parents' in lower or 'siblings' in lower or 'cousin' in lower or 'aunt' in lower or 'uncle' in lower or 'grandma' in lower or 'son' in lower or 'daughter' in lower or 'children' in lower:
        return 'fas fa-users'
    elif 'flag' in lower or 'independence' in lower or 'republic' in lower:
        return 'fas fa-flag'
    elif 'holiday' in lower or 'celebration' in lower:
        return 'fas fa-gift'
    else:
        return 'fas fa-calendar-star'

def get_color(day_name):
    """Get color for day"""
    lower = day_name.lower()
    # Food & Drink
    if any(word in lower for word in ['pizza', 'chocolate', 'coffee', 'ice cream', 'burger', 'pasta', 'cookie', 'cake', 'pie', 'nutella', 'popcorn', 'brownie', 'cheese', 'salami', 'donut', 'cider', 'beer', 'daiquiri', 'rum', 'eggnog', 'bacon', 'tuna', 'hamburger', 'avocado', 'watermelon', 'coconut', 'corn', 'carrot', 'pumpkin']):
        return '#FF6B6B'  # Red
    # Animals & Nature
    elif any(word in lower for word in ['bird', 'penguin', 'squirrel', 'dragon', 'elephant', 'bat', 'turtle', 'snake', 'cat', 'dog', 'pet', 'animal', 'wildlife', 'monkey', 'tree', 'plant', 'flower', 'garden', 'vegetable', 'carrot', 'pumpkin']):
        return '#4CAF50'  # Green
    # Science & Tech
    elif any(word in lower for word in ['science', 'fiction', 'inventor', 'dna', 'space', 'moon', 'planet', 'rocket', 'computer', 'internet', 'camera', 'photography', 'video', 'emoji', 'typewriter', 'scrabble', 'morse', 'calculator', 'mathematics', 'pi', 'fibonacci', 'chemistry', 'molecule', 'physics', 'geek', 'programmer', 'ninja']):
        return '#2196F3'  # Blue
    # Arts & Culture
    elif any(word in lower for word in ['art', 'music', 'dance', 'theatre', 'poetry', 'book', 'reading', 'literacy', 'language', 'grammar', 'punctuation', 'braille', 'crayon']):
        return '#9C27B0'  # Purple
    # Love & Relationships
    elif any(word in lower for word in ['love', 'valentine', 'heart', 'friendship', 'family', 'mother', 'father', 'parents', 'siblings']):
        return '#E91E63'  # Pink
    # Holidays & Observances
    elif any(word in lower for word in ['new year', 'christmas', 'easter', 'thanksgiving', 'halloween', 'holiday', 'independence', 'republic', 'remembrance']):
        return '#FF9800'  # Orange
    # Health & Wellness
    elif any(word in lower for word in ['health', 'doctor', 'nurse', 'dentist', 'sleep', 'yoga', 'exercise', 'mental', 'cancer', 'diabetes', 'hepatitis', 'sickle', 'tuberculosis', 'autism', 'disability', 'aids', 'tobacco', 'drug', 'alcohol']):
        return '#00BCD4'  # Cyan
    # Miscellaneous
    else:
        return '#6a11cb'  # Default Purple

def get_animation(day_name):
    """Get animation for day"""
    lower = day_name.lower()
    if 'new year' in lower or 'christmas' in lower or 'independence' in lower:
        return 'fireworks'
    elif 'valentine' in lower or 'love' in lower or 'heart' in lower:
        return 'hearts'
    elif 'space' in lower or 'moon' in lower or 'planet' in lower or 'rocket' in lower:
        return 'space'
    elif any(word in lower for word in ['bird', 'cat', 'dog', 'pet', 'animal', 'wildlife', 'monkey']):
        return 'animals'
    elif any(word in lower for word in ['pizza', 'chocolate', 'coffee', 'ice cream', 'burger', 'pasta', 'cookie', 'cake']):
        return 'food'
    elif 'music' in lower or 'dance' in lower:
        return 'music'
    elif 'art' in lower or 'paint' in lower:
        return 'art'
    elif 'peace' in lower or 'dove' in lower:
        return 'peace'
    elif 'science' in lower or 'math' in lower:
        return 'science'
    else:
        return 'default'

def get_category(day_name):
    """Get category for day"""
    lower = day_name.lower()
    if any(word in lower for word in ['pizza', 'chocolate', 'coffee', 'ice cream', 'burger', 'pasta', 'cookie', 'cake', 'pie', 'nutella', 'popcorn', 'brownie', 'cheese', 'salami', 'donut', 'cider', 'beer', 'daiquiri', 'rum', 'eggnog', 'bacon', 'tuna', 'hamburger', 'avocado', 'watermelon', 'coconut', 'corn', 'carrot', 'pumpkin']):
        return 'food'
    elif any(word in lower for word in ['bird', 'penguin', 'squirrel', 'dragon', 'elephant', 'bat', 'turtle', 'snake', 'cat', 'dog', 'pet', 'animal', 'wildlife', 'monkey']):
        return 'animals'
    elif any(word in lower for word in ['science', 'fiction', 'inventor', 'dna', 'space', 'moon', 'planet', 'rocket', 'computer', 'internet', 'camera', 'photography', 'video', 'emoji', 'typewriter', 'scrabble', 'morse', 'calculator', 'mathematics', 'pi', 'fibonacci', 'chemistry', 'molecule', 'physics', 'geek', 'programmer', 'ninja']):
        return 'science-tech'
    elif any(word in lower for word in ['art', 'music', 'dance', 'theatre', 'poetry', 'book', 'reading', 'literacy', 'language', 'grammar', 'punctuation', 'braille', 'crayon']):
        return 'arts-culture'
    elif any(word in lower for word in ['love', 'valentine', 'heart', 'friendship', 'family', 'mother', 'father', 'parents', 'siblings']):
        return 'relationships'
    elif any(word in lower for word in ['new year', 'christmas', 'easter', 'thanksgiving', 'halloween', 'holiday']):
        return 'holidays'
    elif any(word in lower for word in ['health', 'doctor', 'nurse', 'dentist', 'sleep', 'yoga', 'exercise', 'mental', 'cancer', 'diabetes', 'hepatitis', 'sickle', 'tuberculosis', 'autism', 'disability', 'aids', 'tobacco', 'drug', 'alcohol']):
        return 'health'
    elif any(word in lower for word in ['tree', 'plant', 'flower', 'garden', 'vegetable', 'carrot', 'pumpkin']):
        return 'nature'
    else:
        return 'other'

# Enrich the data with metadata
enrich_data()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

# API Routes
@app.route('/api/days', methods=['GET'])
def get_all_days():
    """Get all special days"""
    return jsonify({
        "days": special_days,
        "count": len(special_days),
        "total_views": sum(views_data.values())
    })

@app.route('/api/day/<date>', methods=['GET'])
def get_day(date):
    """Get specific day by date (MM-DD format)"""
    for day in special_days:
        if day['date'] == date:
            # Record view for this day
            views_data[date] += 1
            return jsonify(day)
    return jsonify({"error": "Day not found"}), 404

@app.route('/api/view/<date>', methods=['POST'])
def record_view(date):
    """Record a view for a specific day"""
    views_data[date] += 1
    print(f"✓ View recorded for {date}. Total views: {views_data[date]}")
    return jsonify({
        "message": "View recorded", 
        "date": date, 
        "views": views_data[date]
    })

@app.route('/api/search', methods=['GET'])
def search_days():
    """Search for special days by keyword"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = []
    for day in special_days:
        if (query in day['day'].lower() or 
            query in day.get('description', '').lower() or
            query in day.get('category', '').lower()):
            results.append(day)
    
    # Sort by relevance
    results.sort(key=lambda x: (
        x['day'].lower().startswith(query),
        x['day'].lower().count(query),
        -len(x['day'])
    ), reverse=True)
    
    return jsonify(results[:20])

@app.route('/api/popular', methods=['GET'])
def get_popular():
    """Get most viewed days"""
    popular = []
    for date, views in views_data.items():
        day_info = next((d for d in special_days if d['date'] == date), None)
        if day_info:
            popular.append({
                "date": date,
                "day": day_info['day'],
                "views": views
            })
    
    popular.sort(key=lambda x: x['views'], reverse=True)
    return jsonify(popular[:10])

@app.route('/api/today', methods=['GET'])
def get_today():
    """Get today's special day"""
    today = datetime.now()
    date_str = today.strftime("%m-%d")
    
    for day in special_days:
        if day['date'] == date_str:
            return jsonify(day)
    
    return jsonify({
        "date": date_str,
        "day": f"Day {today.timetuple().tm_yday}",
        "description": "No specific special day today, but every day is special!"
    })

@app.route('/api/upcoming', methods=['GET'])
def get_upcoming():
    """Get upcoming special days (next 10 days)"""
    today = datetime.now()
    current_month = today.month
    current_day = today.day
    
    upcoming = []
    for day in special_days:
        month, day_num = map(int, day['date'].split('-'))
        
        # Check if date is in future (within next 30 days)
        if (month > current_month) or (month == current_month and day_num >= current_day):
            upcoming.append(day)
            if len(upcoming) >= 10:
                break
    
    return jsonify(upcoming)

@app.route('/api/random', methods=['GET'])
def get_random():
    """Get a random special day"""
    if special_days:
        return jsonify(random.choice(special_days))
    return jsonify({"error": "No days available"}), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = {}
    for day in special_days:
        category = day.get('category', 'other')
        if category not in categories:
            categories[category] = []
        categories[category].append(day)
    
    return jsonify(categories)

@app.route('/api/category/<category_name>', methods=['GET'])
def get_by_category(category_name):
    """Get days by category"""
    results = []
    for day in special_days:
        if day.get('category') == category_name:
            results.append(day)
    
    return jsonify(results)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    total_views = sum(views_data.values())
    most_viewed = max(views_data.items(), key=lambda x: x[1]) if views_data else None
    
    # Count by category
    category_count = {}
    for day in special_days:
        category = day.get('category', 'other')
        category_count[category] = category_count.get(category, 0) + 1
    
    return jsonify({
        "total_days": len(special_days),
        "total_views": total_views,
        "unique_days_viewed": len(views_data),
        "most_viewed": {
            "date": most_viewed[0] if most_viewed else None,
            "views": most_viewed[1] if most_viewed else 0
        } if most_viewed else None,
        "category_distribution": category_count
    })

@app.route('/api/update', methods=['POST'])
def update_days():
    """Update special days data (protected endpoint)"""
    # Add authentication in production
    global special_days
    
    try:
        data = request.json
        if not data or 'days' not in data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update the data
        special_days = data['days']
        # Re-enrich data
        enrich_data()
        
        return jsonify({
            "message": f"Updated with {len(special_days)} days",
            "count": len(special_days)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "days_loaded": len(special_days),
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "endpoints": [
            "/api/days",
            "/api/day/<MM-DD>",
            "/api/today",
            "/api/random",
            "/api/search?q=query",
            "/api/popular",
            "/api/upcoming",
            "/api/categories",
            "/api/stats",
            "/api/health"
        ]
    })

@app.route('/api/month/<int:month>', methods=['GET'])
def get_month_days(month):
    """Get all days for a specific month (1-12)"""
    if month < 1 or month > 12:
        return jsonify({"error": "Invalid month. Use 1-12"}), 400
    
    month_days = []
    for day in special_days:
        day_month = int(day['date'].split('-')[0])
        if day_month == month:
            month_days.append(day)
    
    return jsonify({
        "month": month,
        "days": month_days,
        "count": len(month_days)
    })

if __name__ == '__main__':
    print("=" * 70)
    print("365-DAY SPECIAL CALENDAR API")
    print("=" * 70)
    print(f"✓ Loaded {len(special_days)} special days")
    print(f"✓ Data enriched with icons, colors, animations, and categories")
    print("\n" + "=" * 70)
    print("SERVER STARTING...")
    print(f"URL: http://localhost:5000")
    print("\nAPI ENDPOINTS:")
    print("  GET  /api/days              - Get all 365 special days")
    print("  GET  /api/day/<MM-DD>       - Get specific day (e.g., /api/day/01-01)")
    print("  GET  /api/today             - Get today's special day")
    print("  GET  /api/random            - Get random special day")
    print("  GET  /api/search?q=query    - Search days")
    print("  GET  /api/popular           - Most viewed days")
    print("  GET  /api/upcoming          - Next 10 upcoming days")
    print("  GET  /api/categories        - Get all categories")
    print("  GET  /api/category/<name>   - Get days by category")
    print("  GET  /api/month/<1-12>      - Get days for specific month")
    print("  GET  /api/stats             - Statistics")
    print("  GET  /api/health            - Health check")
    print("  POST /api/view/<MM-DD>      - Record a view")
    print("\nFRONTEND:")
    print("  GET  /                      - Main calendar interface")
    print("=" * 70)
    
    # Save data to file for backup
    try:
        with open('special_days_backup.json', 'w', encoding='utf-8') as f:
            json.dump(special_days, f, indent=2, ensure_ascii=False)
        print("✓ Backup saved to special_days_backup.json")
    except Exception as e:
        print(f"✗ Could not save backup: {e}")
    
    print("\nStarting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)