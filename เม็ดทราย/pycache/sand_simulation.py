import pygame
import random
import math

# ตั้งค่าเบื้องต้น
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.2
FRICTION = 0.95  # การสูญเสียพลังงานจากการชน
SAND_RADIUS = 3
PARTICLE_COLOR = (194, 178, 128) # สีทราย

class SandParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1) # ความเร็วต้นแนวแกน X
        self.vy = 0 # ความเร็วต้นแนวแกน Y
        self.stopped = False

    def move(self, others):
        if self.stopped:
            return

        # คำนวณความเร็วจากแรงโน้มถ่วง
        self.vy += GRAVITY
        
        # อัปเดตตำแหน่ง
        self.x += self.vx
        self.y += self.vy

        # ตรวจสอบการกระทบพื้น
        if self.y >= HEIGHT - SAND_RADIUS:
            self.y = HEIGHT - SAND_RADIUS
            self.vy *= -0.2 # กระดอนเล็กน้อย
            self.vx *= FRICTION # แรงเสียดทานที่พื้น
            if abs(self.vy) < 0.5: self.vy = 0

        # ตรวจสอบการชนกับเม็ดทรายเม็ดอื่น (Simple Collision)
        for other in others:
            if other is self: continue
            
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < SAND_RADIUS * 2:
                # เกิดการเบียดออกด้านข้าง (Lateral Flow)
                overlap = (SAND_RADIUS * 2) - distance
                angle = math.atan2(dy, dx)
                
                # ผลักออกในทิศทางตรงกันข้าม
                self.x -= math.cos(angle) * overlap * 0.5
                self.y -= math.sin(angle) * overlap * 0.5
                
                # ถ่ายโอนโมเมนตัมแบบง่าย
                self.vx *= FRICTION
                self.vy *= FRICTION

    def draw(self, screen):
        pygame.draw.circle(screen, PARTICLE_COLOR, (int(self.x), int(self.y)), SAND_RADIUS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    particles = []
    running = True
    
    while running:
        screen.fill((30, 30, 30)) # พื้นหลังสีเข้ม
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ปล่อยทรายจากจุดกึ่งกลางด้านบน (จำลองทรายตก)
        if len(particles) < 500: # จำกัดจำนวนเพื่อไม่ให้หน่วง
            particles.append(SandParticle(WIDTH // 2 + random.uniform(-5, 5), 50))

        # อัปเดตและวาดเม็ดทราย
        for p in particles:
            p.move(particles)
            p.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()