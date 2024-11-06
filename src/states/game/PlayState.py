from src.states.BaseState import BaseState
import pygame, sys
from src.recourses import *
from src.constants import *
from src.entity_defs import *

from src.entity_defs import EntityConf
from src.player import Player

from src.states.entity.player.PlayerWalkState import PlayerWalkState
from src.states.entity.player.PlayerIdleState import PlayerIdleState
from src.states.entity.player.PlayerAttackState import PlayerAttackState
from src.StateMachine import StateMachine

# from src.world.Dungeon import Dungeon
from src.World import World


class PlayState(BaseState):
    def __init__(self):
        pass

    def Enter(self, params):
        self.paused = False
        entity_conf = ENTITY_DEFS["player"]
        self.player = Player(entity_conf)
        self.world = World(self.player)

        self.player.state_machine = StateMachine()
        self.player.state_machine.SetScreen(pygame.display.get_surface())
        self.player.state_machine.SetStates(
            {
                "walk": PlayerWalkState(self.player, self.dungeon),
                "idle": PlayerIdleState(self.player),
                "swing_sword": PlayerAttackState(self.player, self.dungeon),
            }
        )

        self.player.ChangeState("walk")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # กด p เพื่อ pause/resume
                if event.key == pygame.K_p:
                    self.paused = True

        # ถ้า paused -- โดน return ตัดจบ
        if self.paused:
            # ทำสามอัน: resume / retry (เริ่มด่าน 1 ใหม่) / quit
            # 0 = resume / 1 = retry / 2 = quit
            pause_option = 0  # default option
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:  # go up
                        pause_option = [2, 0, 1][pause_option]
                    if event.key == pygame.K_s:  # go down
                        pause_option = [1, 2, 0][pause_option]
                    if event.key == pygame.K_RETURN:  # กด enter
                        if pause_option == 0:
                            self.paused = False
                        if pause_option == 1:
                            # เริ่มใหม่ตั้งแต่ด่านแรก
                            pass
                        if pause_option == 2:
                            pygame.quit()
                            sys.exit()

            return

        self.World.update(dt, events)

        if self.player.health == 0:
            g_state_manager.Change("game_over")

        # temp
        # self.room.update(dt, events)

    def render(self, screen):
        # dungen render
        self.World.render(screen)

        # ใส่ stats ต่างๆ ภายในเกม ตรงด้านบนจอ
        # Ex. Health, Enemy Remaining, etc.

        '''
        health_left = self.player.health

        for i in range(3):
            if health_left > 1:
                heart_frame = 2
            elif health_left ==1:
                heart_frame = 1
            else:
                heart_frame = 0

            screen.blit(gHeart_image_list[heart_frame], (i * (TILE_SIZE+3), 6))
            health_left -=2

        '''

        # temp
        # self.room.render(screen)
        if self.paused:
            # ถมจอดำ ทำหน้า pause พร้อมสามออปชั่น
            """
            t_pause = gFonts['large'].render("PAUSED", False, (255, 255, 255))
            rect = t_pause.get_rect(center = (WIDTH/2, HEIGHT/2))
            screen.blit(t_pause, rect)
            """
            pass

    def Exit(self):
        pass
