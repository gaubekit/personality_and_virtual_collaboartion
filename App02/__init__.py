from otree.api import *
import time

c = cu

doc = ' Spider Graph + WLG Intro & Control Questions? + WLG'


class C(BaseConstants):
    NAME_IN_URL = 'App02'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ENDOWMENT = 200


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    groupMin = models.IntegerField(
        min=0, max=40, initial=40
    )
    randomNumber = models.IntegerField()


def make_field6(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6],
        label=label,
        widget=widgets.RadioSelectHorizontal,
    )


def make_field(label):
    return models.IntegerField(
        choices=[0, 10, 20, 30, 40],
        label=label,
        widget=widgets.RadioSelect,
    )


def waiting_too_long(player):
    participant = player.participant
    return time.time() - participant.wait_page_arrival > 60  # * 10 # TODO ADD 10 for 10 Minutes!


def group_by_arrival_time_method(subsession, waiting_players):
    print(waiting_players)
    if len(waiting_players) >= 3:
        return waiting_players[:3]
    for player in waiting_players:
        print('test: ', player)
        print(player.participant.single_player)
        if waiting_too_long(player):
            player.participant.single_player = True
            return [player]


class Player(BasePlayer):
    ownDecision_subround1 = make_field("Please choose one")
    payoff_hypo_subround1 = models.IntegerField()

    most_important_goal = models.StringField(
                 choices=[['vm_pref_achievement', 'Ensuring Compliance with Rules'],
                          ['vm_pref_dominance', 'Advocating for Justice and Fairness'],
                          ['vm_pref_face', 'Demonstrating Openness and Understanding'],
                          ['vm_pref_rules', 'Presenting Success in the Meeting'],
                          ['vm_pref_concern', 'Exercising Influence and Control'],
                          ['vm_pref_tolerance', 'Maintaining My Public Image']],
                 label='If you had to name out of this six preferences one goal for the upcoming video meeting, which one would it be?*')

    # TODO: Was beeinflusste die Entscheidung?
    # TODO: Macht nur Sinn in Treatment -> Wie Frage ich Einfluss auf Goal und Expectations ab?
    # oder kontinnum von expectation zu goal als gegenüberstellung?
    # Was beeinflusste deine Entscheidung? Mein Ziel, eher mein Ziel,weder Ziel noch Erwartungen, eher Erwartungen, Erwartungen
    # my own goals VS the goals of others?
    team_goal = make_field6(
        'To what extent was it your goal to collaborate?') # TODO
    team_expectation = make_field6(
        'To what extent do you expect your team members have collaborated?') # TODO


class MyWaitPage(WaitPage):
    """ group participants"""
    group_by_arrival_time = True
    #
    # @staticmethod
    # def app_after_this_page(player, upcoming_apps):
    #     if player.participant.single_player:
    #         return 'App03'


class TeamGoals(Page):
    """ This page shows the VM preferences in a Spider Graph and made the Participant to select the most important goal"""
    form_model = 'player'
    form_fields = ['most_important_goal']

    @staticmethod
    def is_displayed(player):
        print(player.participant.single_player)
        return not player.participant.single_player

    @staticmethod
    def js_vars(player):
        others = player.get_others_in_group()
        return dict(
            own=[player.participant.vm_pref_achievement,
                 player.participant.vm_pref_dominance,
                 player.participant.vm_pref_face,
                 player.participant.vm_pref_rules,
                 player.participant.vm_pref_concern,
                 player.participant.vm_pref_tolerance],
            other1=[others[0].participant.vm_pref_achievement,
                    others[0].participant.vm_pref_dominance,
                    others[0].participant.vm_pref_face,
                    others[0].participant.vm_pref_rules,
                    others[0].participant.vm_pref_concern,
                    others[0].participant.vm_pref_tolerance],
            other2=[others[1].participant.vm_pref_achievement,
                    others[1].participant.vm_pref_dominance,
                    others[1].participant.vm_pref_face,
                    others[1].participant.vm_pref_rules,
                    others[1].participant.vm_pref_concern,
                    others[1].participant.vm_pref_tolerance]
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        #players = player.group.get_player_by_id()

        if not player.participant.single_player:
            players = player.group.get_players()

            players[0].participant.svo_other = players[2].participant.svo_to_other
            players[2].participant.svo_other = players[1].participant.svo_to_other
            players[1].participant.svo_other = players[0].participant.svo_to_other




class Description1(Page):
    """ Page informs the participants about the number of sub-round"""
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return not player.participant.single_player


class Decision1(Page):
    form_model = 'player'
    form_fields = ['ownDecision_subround1']

    @staticmethod
    def is_displayed(player):
        return not player.participant.single_player

    @staticmethod
    def live_method(player: Player, data):
        if "ownDecision_subround1" in data:
            player.ownDecision_subround1 = data["ownDecision_subround1"]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_num=player.round_number)


class CalculatePayoff1(WaitPage):
    body_text = "Please wait until your team members have made their decision."

    @staticmethod
    def is_displayed(player):
        return not player.participant.single_player

    def vars_for_template(self):
        # Get the number of players who have arrived (decided) in the group
        arrived_players = [p for p in self.group.get_players() if p.field_maybe_none('ownDecision_subround1') is not None]
        waiting_count = len(arrived_players)

        return {
            'reload_interval': 5000,  # 5000 milliseconds = 5 seconds
            'waiting_count': waiting_count
        }

    def get_template_name(self):
        return 'global/MyWaitPage.html'

    def js_vars(self):
        return {
            'reload_interval': 5000  # 5000 milliseconds = 5 seconds
        }

    @staticmethod
    def after_all_players_arrive(group: Group):
        # Calculate group minimum and individual payoffs
        group.groupMin = min(p.ownDecision_subround1 for p in group.get_players())

        for p in group.get_players():
            p.payoff_hypo_subround1 = C.ENDOWMENT + (10 * group.groupMin) - (5 * p.ownDecision_subround1)

            # participant variables for payout info
            p.participant.wlg_payoff = p.payoff_hypo_subround1
            p.participant.wlg_min_choice = group.groupMin
            p.participant.wlg_own_choice = p.ownDecision_subround1


class IntroQuestionnaire(Page):
    form_model = 'player'
    form_fields = ['team_goal', 'team_expectation']

    @staticmethod
    def is_displayed(player):
        return not player.participant.single_player


class EndApp02(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return not player.participant.single_player


class EndApp02ByPass(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.participant.single_player


page_sequence = [
    MyWaitPage,
    TeamGoals,
    Description1,
    Decision1,
    CalculatePayoff1,
    IntroQuestionnaire,
    EndApp02,
    EndApp02ByPass
]
