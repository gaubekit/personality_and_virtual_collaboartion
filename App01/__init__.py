from otree.api import *
import math
import time

c = cu
doc = ('''

This App contains
- Welcome, experiment overview and consent
- social value orientation and general mental model
- main video meeting preferences
- Introduction to Weakest Link Game + Comprehension

''')


class C(BaseConstants):
    NAME_IN_URL = 'App01'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    svo_values = dict(
        # Primary I
        C11=[85, 85, 85, 85, 85, 85, 85, 85, 85],  # you
        C21=[85, 76, 68, 59, 50, 41, 33, 24, 15],  # other

        # Primary II
        C12=[85, 87, 89, 91, 93, 94, 96, 98, 100],  # you
        C22=[15, 19, 24, 28, 33, 37, 41, 46, 50],  # other

        # Primary III
        C13=[50, 54, 59, 63, 68, 72, 76, 81, 85],  # you
        C23=[100, 98, 96, 94, 93, 91, 89, 87, 85],  # other

        #  Primary IV
        C14=[50, 54, 59, 63, 68, 72, 76, 81, 85],  # you
        C24=[100, 89, 79, 68, 58, 47, 36, 26, 15],  # other


        # Primary V
        C15=[100, 94, 88, 81, 75, 69, 63, 56, 50],  # you
        C25=[50, 56, 63, 69, 75, 81, 88, 94, 100],  # other

        # Primary IV
        C16=[100, 98, 96, 94, 93, 91, 89, 87, 85],  # you
        C26=[50, 54, 59, 63, 68, 72, 76, 81, 85],  # other


        # Secondary Items
        # C17=[100, 96, 93, 89, 85, 81, 78, 74, 70],
        # C27=[50, 56, 63, 69, 75, 81, 88, 94, 100],
        # C18=[90, 91, 93, 94, 95, 96, 98, 99, 100],
        # C28=[100, 99, 98, 96, 95, 94, 93, 91, 90],
        # C19=[100, 94, 88, 81, 75, 69, 63, 56, 50],
        # C29=[70, 74, 78, 81, 85, 89, 93, 96, 100],
        # C110=[100, 99, 98, 96, 95, 94, 93, 91, 90],
        # C210=[70, 74, 78, 81, 85, 89, 93, 96, 100],
        # C111=[70, 74, 78, 81, 85, 89, 93, 96, 100],
        # C211=[100, 96, 93, 89, 85, 81, 78, 74, 70],
        # C112=[50, 56, 63, 69, 75, 81, 88, 94, 100],
        # C212=[100, 99, 98, 96, 95, 94, 93, 91, 90],
        # C113=[50, 56, 63, 69, 75, 81, 88, 94, 100],
        # C213=[100, 94, 88, 81, 75, 69, 63, 56, 50],
        # C114=[100, 96, 93, 89, 85, 81, 78, 74, 70],
        # C214=[90, 91, 93, 94, 95, 96, 98, 99, 100],
        # C115=[90, 91, 93, 94, 95, 96, 98, 99, 100],
        # C215=[100, 94, 88, 81, 75, 69, 63, 56, 50]
    )


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_6_point_likert_skale_horizontal(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5, 6], widget=widgets.RadioSelectHorizontal)


class Player(BasePlayer):
    consent = models.IntegerField(blank=False, choices=[[0, '0'], [1, '1']], label='Consent',
                                  attrs={"invisible": True})

    # Social Value Orientation
    q1_svo = models.IntegerField()
    q2_svo = models.IntegerField()
    q3_svo = models.IntegerField()
    q4_svo = models.IntegerField()
    q5_svo = models.IntegerField()
    q6_svo = models.IntegerField()
    svo_self = models.FloatField()
    svo_other = models.FloatField()
    svo_ratio = models.FloatField()
    svo = models.FloatField()
    svo_angle = models.FloatField()
    svo_type = models.StringField()

    # General Mental Model
    collaborative_goal = make_6_point_likert_skale_horizontal(
        'On a scale from 1 (not at all) to 6 (very much): In general, to what extent would you rate your goal to collaborate?')
    collaboration_expectations = make_6_point_likert_skale_horizontal(
        'On a scale from 1 (not at all) to 6 (very much): In general, to what extent would you expect others to collaborate?')

    # Video Meeting Behavor Preferences TODO: SIND DAS DIE FINALEN PRÄFERENZEN?
    vm_achievement = make_6_point_likert_skale_horizontal(
        'In video meetings, I want to ensure that my public reputation remains intact by avoiding mistakes and protecting myself from potential embarrassment'
    )
    vm_power_dominance = make_6_point_likert_skale_horizontal(
        'In video meetings, I aim to strengthen my control over material and social resources to reinforce my position and decision-making power.'
    )
    vm_face = make_6_point_likert_skale_horizontal(
        'In video meetings, I want to ensure that my public reputation remains intact by avoiding mistakes and protecting myself from potential embarrassment'
    )
    vm_conformity_rules = make_6_point_likert_skale_horizontal(
        'In video meetings, my goal is to adhere to all regulations, laws, and formal obligations in the meeting and encourage others to do the same'
    )
    vm_universalism_concern = make_6_point_likert_skale_horizontal(
        'In video meetings, I want to promote equality, justice, and the protection of all people by emphasizing these values in the discussion.'
    )
    vm_universalism_tolerance = make_6_point_likert_skale_horizontal(
        'I strive to create an inclusive and respectful atmosphere by accepting and actively supporting different opinions and perspectives.'
    )

    # Comprehension Weakest Link Game
    comp1_check = models.IntegerField(initial=0)
    comp2_check = models.IntegerField(initial=0)
    comp3_check = models.IntegerField(initial=0)
    comp4_check = models.IntegerField(initial=0)
    comprehension1 = models.IntegerField(
        label='<br><strong>What would be your compensation if you work 0 hours on Project A '
              'and the lowest contribution of a team member to Project A is 10 hours?</strong>', min=0, max=400)
    comprehension2 = models.IntegerField(
        label='<br><strong>What would be your compensation if you work 20 hours on Project A '
              'and the lowest contribution of a team member to Project A is 10 hours?</strong>', min=0, max=400)
    comprehension3 = models.IntegerField(
        label='<br><strong>What would be your compensation if you work 40 hours on Project A '
              'and the lowest contribution of a team member to Project A is 30 hours?</strong>', min=0, max=400)
    comprehension4a = models.BooleanField(
        default=False,
        label='',
        widget=widgets.CheckboxInput,
        blank=True
    )
    comprehension4b = models.BooleanField(
        default=False,
        label='',
        widget=widgets.CheckboxInput,
        blank=True
    )
    comprehension4c = models.BooleanField(
        default=False,
        label='',
        widget=widgets.CheckboxInput,
        blank=True)


# Functions for error messages in comprehension questions
def comprehension1_error_message(player: Player, value):
    if value != 200:
        player.comp1_check += 1
        if player.comp1_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        if player.comp1_check >= 2:
            return "Unfortunately, that's incorrect. The correct answer is <strong>200</strong>."
    return None  # Allow the participant to try again if they haven't clicked incorrectly twice


def comprehension2_error_message(player: Player, value):
    if value != 200:
        player.comp2_check += 1
        if player.comp2_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp2_check >= 2:
            return "Unfortunately, that's incorrect. The correct answer is <strong>200</strong>."
    return None


def comprehension3_error_message(player: Player, value):
    if value != 300:
        player.comp3_check += 1
        if player.comp3_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp3_check >= 2:
            return "Unfortunately, that's incorrect. The correct answer is <strong>300</strong>."
    return None


def comprehension4a_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."
    return None


def comprehension4b_error_message(player: Player, value):
    if value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."
    return None


def comprehension4c_error_message(player: Player, value):
    if not value:
        player.comp4_check += 1
        if player.comp4_check == 1:
            return "Unfortunately, that's incorrect. Please try again."
        elif player.comp4_check >= 2:
            return "Unfortunately, that's incorrect. Your compensation depends on the <strong>number of hours you work on Project A</strong> and the <strong>fewest number of hours worked by a member of your team on Project A</strong>."
    return None


# In the following the Pages of APP01 are defined
class GeneralInformation(Page):
    """ Welcome """
    form_model = 'player'

    @staticmethod
    def before_next_page(player, timeout_happened):
        """ set single player var for waite page - will be changed to True, if no group forms"""
        player.participant.single_player = False


class ExperimentInformation(Page): # TODO MAKE IT SHINY
    """ Experiment Overview """
    form_model = 'player'


class ConsentFormA(Page):
    """ Data Protection, Chair, etc """
    form_model = 'player'


class ConsentFormB(Page):
    """ Consent -> if not, exit - no payout """
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened:
            player.participant.consent = player.consent

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.consent == 0:
            return 'App04'


class IntroSVO(Page):
    """ This page introduces the Social Value Orientation"""
    pass


class SurveySVO(Page):
    """ This Page Measures the Social Value Orientation and Calculates all Valeus"""
    form_model = 'player'
    form_fields = ['q1_svo', 'q2_svo', 'q3_svo', 'q4_svo', 'q5_svo', 'q6_svo']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            **C.svo_values
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        svo_values = C.svo_values

        player.svo_self = (svo_values['C11'][player.q1_svo - 1] +
                           svo_values['C12'][player.q2_svo - 1] +
                           svo_values['C13'][player.q3_svo - 1] +
                           svo_values['C14'][player.q4_svo - 1] +
                           svo_values['C15'][player.q5_svo - 1] +
                           svo_values['C16'][player.q6_svo - 1]) / 6

        player.svo_other = (svo_values['C21'][player.q1_svo - 1] +
                            svo_values['C22'][player.q2_svo - 1] +
                            svo_values['C23'][player.q3_svo - 1] +
                            svo_values['C24'][player.q4_svo - 1] +
                            svo_values['C25'][player.q5_svo - 1] +
                            svo_values['C26'][player.q6_svo - 1]) / 6

        player.svo_ratio = (player.svo_other - 50) / (player.svo_self - 50)
        player.svo_angle = math.degrees(math.atan(player.svo_ratio))

        if player.svo_ratio >= 1.5488:
            player.svo = 1
            player.svo_type = 'Altruism'
        elif 0.441 < player.svo_ratio < 1.5488:
            player.svo = 2
            player.svo_type = 'Prosocial'
        elif -0.213 <= player.svo_ratio <= 0.441:
            player.svo = 3
            player.svo_type = 'Individualistic'
        elif player.svo_ratio < -0.213:
            player.svo = 4
            player.svo_type = 'Competitive'

        player.participant.svo_self = round(player.svo_self, 2)
        player.participant.svo_to_other = round(player.svo_other, 2)
        player.participant.svo_other = None  # will be changed in App02 if team forms


class MentalModel(Page):
    """ This Page assesses the mental model -> Expectations VS Goal"""
    form_model = 'player'
    form_fields = ['collaborative_goal', 'collaboration_expectations']


class VideomeetingBehaviorI(Page):
    """ This is the first part of rating video meeting preferences"""

    form_model = 'player'
    form_fields = ['vm_achievement', 'vm_power_dominance', 'vm_face',
                   'vm_conformity_rules', 'vm_universalism_concern', 'vm_universalism_tolerance']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vm_pref_achievement = player.vm_achievement
        player.participant.vm_pref_dominance = player.vm_power_dominance
        player.participant.vm_pref_face = player.vm_face
        player.participant.vm_pref_rules = player.vm_conformity_rules
        player.participant.vm_pref_concern = player.vm_universalism_concern
        player.participant.vm_pref_tolerance = player.vm_universalism_tolerance

        # initialize predefined goals as session variable
        player.session.vm_goal_labels = [
            ['Presenting Success', 'in the Meeting'],
            ['Exercising', ' Influence', 'and Control'],
            ['Maintaining', 'My Public Image'],
            ['Ensuring', 'Compliance with Rules'],
            ['Advocating for', 'Justice and Fairness'],
            ['Demonstrating ', 'Openness and', 'Understanding']
        ]

class StudyIntroduction1(Page):
    """ This Page Explains the Context of the WLG """
    form_model = 'player'


class StudyIntroduction2(Page):
    """ This Page Explains the Payout of the WLG"""
    form_model = 'player'


class Comprehension1(Page):
    form_model = 'player'
    form_fields = ['comprehension1']


class Comprehension2(Page):
    form_model = 'player'
    form_fields = ['comprehension2']


class Comprehension3(Page):
    form_model = 'player'
    form_fields = ['comprehension3']


class Comprehension4(Page):
    form_model = 'player'
    form_fields = ['comprehension4a', 'comprehension4b', 'comprehension4c']


class EndApp01(Page):
    """ This page informs participant about the process (next wait page)"""
    form_model = 'player'

    @staticmethod
    def before_next_page(player, timeout_happened):
        """ store time when entering waitpage in participant field, to control for time on wait page"""
        player.participant.wait_page_arrival = time.time()


page_sequence = [
    GeneralInformation,
    ExperimentInformation,
    ConsentFormA,
    ConsentFormB,
    IntroSVO,
    SurveySVO,
    MentalModel,
    VideomeetingBehaviorI,
    StudyIntroduction1,
    StudyIntroduction2,
    Comprehension1,
    Comprehension2,
    Comprehension3,
    Comprehension4,
    EndApp01
]
