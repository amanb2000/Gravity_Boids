import math
import random
from vec_funcs import *

class Gboid:
    def __init__(self, WIDTH, HEIGHT, FR):
        self.fr = FR
        self.size = 6
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.px = int(random.uniform(0, WIDTH))
        self.py = int(random.uniform(0, WIDTH))
        self.vx = (random.random() - 0.5)
        self.vy = (random.random() - 0.5)
        self.ax = 0
        self.ay = 0


    def evolve(self, boids, planets):
        """Applying velocity"""
        self.px += (self.vx/self.fr)
        self.py += (self.vy/self.fr)

        self.px = self.px % self.WIDTH
        self.py = self.py % self.HEIGHT

        """Applying acceleration"""
        MAX_VELOCITY = 60
        MAX_ACCELERATION = 60

        self.vx+=(self.ax/self.fr) 
        self.vy+=(self.ay/self.fr) 

        velocity = math.sqrt(self.vx**2 + self.vy**2)

        if velocity > MAX_VELOCITY:
            factor = MAX_VELOCITY/velocity
            self.vx *= factor
            self.vy *= factor

        """
        === Applying other effects ===
        Conventional Boid Effects:
            1. Separation from immediate neighbours: Defined by a 'safety zone'.
            2. Alignment toward the direction of nearby neighbours: Defined by an 'alignment radius'
            3. Cohesion toward the center of mass of flock mates: Defined by 'flock radius'

        Additional Experimental Effects:
            1. Planetary gravity
            2. Stationary gravitational objects
            3. Different kinds of decay functions (as opposed to static radii)
        """
        SAFETY_ZONE = 200
        ALIGNMENT_RAD = 200
        FLOCK_RAD = 300

        SAFETY_WEIGHT = -3
        ALIGNMENT_WEIGHT = 0.5
        FLOCK_WEIGHT = 0.2

        

        safety_vec = [0, 0] # Sum -> Average of the center of mass of the boids within the minimum safe distance
        num_safety_boids = 0

        alignment_vec = [0, 0] # Sum -> average of the VELOCITIES of the boids within the alignment radius
        num_alignment_boids = 0

        flock_vec = [0, 0] # Sum -> average of the center of mass of the boids within the flocking radius
        num_flock_boids = 0

        for i in boids:
            dist = get_dist([i.px, i.py], [self.px, self.py])

            if dist < SAFETY_ZONE:
                safety_vec[0] += i.px
                safety_vec[1] += i.py
                num_safety_boids += 1

            if dist < ALIGNMENT_RAD:
                alignment_vec[0] += i.vx
                alignment_vec[1] += i.vy
                num_alignment_boids += 1

            if dist < FLOCK_RAD:
                flock_vec[0] += i.px
                flock_vec[1] += i.py
                num_flock_boids += 1

        safety_vec[0] /= (num_safety_boids)
        safety_vec[1] /= (num_safety_boids)

        safety_vec[0] = (safety_vec[0] - i.px)
        safety_vec[1] = (safety_vec[1] - i.py)

        safety_mag = math.sqrt(safety_vec[0]**2 + safety_vec[1]**2)

        if safety_mag != 0:
            safety_vec[0] *= safety_vec[0]*(SAFETY_WEIGHT/safety_mag)
            safety_vec[1] *= safety_vec[1]*(SAFETY_WEIGHT/safety_mag)


        alignment_vec[0] *= (1/num_alignment_boids)
        alignment_vec[1] *= (1/num_alignment_boids)

        alignment_mag = math.sqrt(alignment_vec[0]**2 + alignment_vec[1]**2)

        if alignment_mag != 0:
            alignment_vec[0] *= (ALIGNMENT_WEIGHT/alignment_mag)
            alignment_vec[1] *= (ALIGNMENT_WEIGHT/alignment_mag)

        
        flock_vec[0] /= num_flock_boids
        flock_vec[1] /= num_flock_boids

        flock_vec[0] = (flock_vec[0] - i.px)
        flock_vec[1] = (flock_vec[1] - i.py)

        flock_mag = math.sqrt(flock_vec[0]**2 + flock_vec[1]**2)

        if flock_mag != 0:
            flock_vec[0] *= (FLOCK_WEIGHT/flock_mag)
            flock_vec[1] *= (FLOCK_WEIGHT/flock_mag)


        self.ax = safety_vec[0] + alignment_vec[0] + flock_vec[0]
        self.ay = safety_vec[1] + alignment_vec[1] + flock_vec[1]

        acceleration = math.sqrt(self.ax**2 + self.ay**2)


        if(acceleration > MAX_ACCELERATION):
            factor = MAX_ACCELERATION/acceleration
            self.ax *= factor
            self.ay *= factor

        """PLANETARY GRAVITY"""
        G = -5000
        m = 1
        
        planet_acc = [0, 0]

        for i in planets:
            force = G*m*i.mass
            dist = math.sqrt( (i.py - self.py)**2 + (i.px - self.px)**2 )
            force /= (dist**2)

            acc_vec = get_unit_a_to_b([self.px, self.py], [i.px, i.py])

            acc_vec[0] *= force
            acc_vec[1] *= force

            planet_acc[0] += acc_vec[0]
            planet_acc[1] += acc_vec[1]

        self.ax += planet_acc[0]
        self.ay += planet_acc[1]


        


        





        