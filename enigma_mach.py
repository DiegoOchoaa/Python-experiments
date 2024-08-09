
import pygame, sys, random,clipboard

def rotate_rotor(rotor):
     first_char = rotor[0]
     rotor = rotor[1:]
     rotor = rotor + first_char
     return rotor

def rotate_rotor_reverse(rotor):
    last_char = rotor[-1]
    rotor = last_char + rotor[:-1]
    return rotor

def display_text(text,x2,y2,color,font):
        score_surface = font.render(f"{text}",False,(color))
        score_rect = score_surface.get_rect(center=(x2,y2))
        screen.blit(score_surface, score_rect)

def display_reflector(x,letter_pressed):
    global reflector,before_reflexion
    first_row = reflector[0]
    second_row = reflector[1]

    
    for letter in first_row:
        if letter == letter_pressed:
            color = ((50, 102, 168))
        elif letter == before_reflexion:
             color = ((168, 50, 50))
    
        else: color = ((200,200,200))

        display_text(letter,x,((first_row.index(letter)+4)*40),color,smallfont)   
    for letter in second_row:
        if letter == letter_pressed:
            color = ((50, 102, 168))
        elif letter == before_reflexion:
             color = ((168, 50, 50))
             
        else: color = ((200,200,200))
        display_text(letter,x + 50,((second_row.index(letter)+4)*40),color,smallfont)   
    


def encrypt_word(word, reflector):
    global alphabet, r2, r1, r3,rotor_rotations, letter_reflected,before_reflexion, letter_phase1,letter_phase2,letter_phase3,letter_after1,letter_after2,letter_after3
    encrypted_word = ''
    rotor_1 = r1
    rotor_2 = r2
    rotor_3 = r3
    

    for letter in word:
         
        letter_phase1 = rotor_3[alphabet.index(letter)]

        letter_phase2 = rotor_2[alphabet.index(letter_phase1)]

        letter_phase3 = rotor_1[alphabet.index(letter_phase2)]
        
        before_reflexion = letter_phase3
        reflected = reflect_letter(letter_phase3, reflector)
        letter_reflected = reflected

        letter_after1 = alphabet[rotor_1.index(reflected)]

        letter_after2 = alphabet[rotor_2.index(letter_after1)]
        
        letter_after3 = alphabet[rotor_3.index(letter_after2)]
       
         

        encrypted_word += letter_after3


        
        rotor_1 = rotate_rotor(rotor_1)
        print(rotor_rotations)
        
        if rotor_rotations[0] == 26:
            rotor_2 = rotate_rotor(rotor_2)
            rotor_rotations[0] = 0
            rotor_rotations[1] += 1
        
        if rotor_rotations[1] == 26:
            rotor_3 = rotate_rotor(rotor_3)
            rotor_rotations[1] = 0
        
         
        
    return encrypted_word

def reflect_letter(letter, reflector):  
   try:
        letter_pos = reflector[1].index(letter)
        letter = reflector[0][letter_pos]
   except:
        letter_pos = reflector[0].index(letter)
        letter = reflector[1][letter_pos]
   return letter


def keyboard_functions():
     all_keys = pygame.key.get_pressed()
     abc = 'qwertyuiopasdfghjklzxcvbnm'
     for letter in range(len(abc)):
        if  all_keys[getattr(pygame, 'K_'+ abc[letter])] == True:

            return abc[letter]
def read_keyboard(letter):
     all_keys = pygame.key.get_pressed()
     if  all_keys[getattr(pygame, 'K_'+ letter)] == True:

            return True
     else:
          return False


def print_rotor(rotor,x,letter1,letter2):
     
     for letter in rotor:
        if letter == letter2:
            color = ((50, 102, 168))
            
        elif letter == letter1:
            color = ((168, 50, 50))
         
        else: 
            color = ((200,200,200))
           
            
        display_text(letter,x,((rotor.index(letter)+7)*20),color,smallfont)   
        


#definitions
 
rotor_rotations = [0,0]
r1  ='jfuzswrbnexpdlycokmtv qihga'
r2  ='ftougnikc pmrhazwxljebvdqys'
r3  = ' cwmizhalsneqtbugjkxpyovfdr'
letter_phase1,letter_phase2,letter_phase3,letter_after1,letter_after2,letter_after3 = '','','','','',''
process = [letter_phase1,letter_phase2,letter_phase3,letter_after1,letter_after2,letter_after3]
show1 = r1
show2 = r2
show3 = r3
before_reflexion = ''
letter_reflected = ''
letter_pressed = ''

alphabet = 'abcdefghijklmnopqrstuvwxyz '
reflector = [['y', 'w', 'f', 'z', 'p', 'h', 'g', 'o', 'k', 'q', 'b', 't', 'e', ' '], ['n', 'c', 'd', 's', 'm', 'x', 'u', 'j', 'v', 'i', 'r', 'a', 'l', ' ']]

pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1300, 900
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((screen_width, screen_height))
#PILOWA
#bigfont =  pygame.font.Font('/Users/diegoochoa/Documents/python/enigma/Pilowlava-Regular.otf', 70)
#font =  pygame.font.Font('/Users/diegoochoa/Documents/python/enigma/Pilowlava-Regular.otf', 40)
#smallfont =  pygame.font.Font('/Users/diegoochoa/Documents/python/enigma/Pilowlava-Regular.otf', 25)

bigfont =  pygame.font.Font('/Users/diegoochoa/Documents/python/enigma/MajorMonoDisplay-Regular.ttf', 70)
font =  pygame.font.Font('/Users/diegoochoa/Documents/python/enigma/MajorMonoDisplay-Regular.ttf', 40)
smallfont =  pygame.font.Font('/Users/diegoochoa/Documents/python/enigma/MajorMonoDisplay-Regular.ttf', 25)
smallest =  pygame.font.Font('/Users/diegoochoa/Documents/python/enigma/MajorMonoDisplay-Regular.ttf', 10)
word = ''
encrypted_word = ''
decrypted_word = ''
encrypt_decrypt = True
encry_word = ''


while True: # Game Loop
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
         if event.type == pygame.KEYDOWN:
              if keyboard_functions() != None and keyboard_functions() in alphabet: 
                 letter_pressed = keyboard_functions()
                 word = word + letter_pressed
                 encry_word = encry_word + letter_pressed
                 rotor_rotations[0] += 1

                 

                 show1 = rotate_rotor(show1)
                 print(rotor_rotations)
        
                 if rotor_rotations[0] == 26:
                    show2 = rotate_rotor(show2)
                    rotor_rotations[0] = 0
                    rotor_rotations[1] += 1
        
                 if rotor_rotations[1] == 26:
                    show3 = rotate_rotor(show3)
                    rotor_rotations[1] = 0
        
                
                
              if read_keyboard('SPACE'):
                 word += ' '
                 encry_word += ' '
                 rotor_rotations[0] += 1

              if read_keyboard('BACKSLASH') and word != '':
                 
                 word = list(word)
                 word[len(word)-1] = ''
                 word = ''.join(word)
                 show1 = rotate_rotor_reverse(show1)
                 if rotor_rotations[0] > 0:
                    rotor_rotations[0] -= 1
                 else: 
                     rotor_rotations[1] -= 1
                     rotor_rotations[0] = 25
                     show2 = rotate_rotor_reverse(show2)

              if read_keyboard('DOWN'):
                  word = clipboard.paste()
             
                  
                  
              if read_keyboard('RETURN'):
                 clipboard.copy(encry_word)
                 word = ''
                 encry_word = ''
                 show1 = r1
                 show2 = r2
                 show3 = r3
                 rotor_rotations = [0,0]
         
              


    if True:
         screen.fill((20, 20, 20))
         display_text('eNiGmA',600,100,((255,255,255)),bigfont)
         display_text(word,600,350,((255,255,255)),font)
         
              #ENCRIPTION
         display_text('by Diegö',600,800,((255,255,255)),smallfont)
         display_text((rotor_rotations[0],rotor_rotations[1]),600,840,((255,255,255)),smallest)
         
         encry_word = encrypt_word(word, reflector)
         display_text(encry_word,600,500,((255,255,255)),smallfont)
         print_rotor(show1,1050,letter_phase1,letter_after1)   
         print_rotor(show2,1100,letter_phase2,letter_after2) 
         print_rotor(show3,1150,letter_phase3,letter_after3)
         display_reflector(110,letter_reflected)
         #print(print(letter_phase1,letter_phase2,letter_phase3,letter_after1,letter_after2,letter_after3))


              
        
         
              
        
    pygame.display.flip()
    
    clock.tick(60)