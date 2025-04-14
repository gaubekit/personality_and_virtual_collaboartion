import random
from otree.api import *


doc = """
Demographics, Rest of Meeting Goals, PVQ, ThankYou and PayoutInfo
"""


class C(BaseConstants):
    NAME_IN_URL = 'App03'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    FIX_PAYOFF = 400


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def pvq_scale_calc(pvq1, pvq2, pvq3):
    return pvq1 + pvq2 + pvq3


def make_6_point_likert_skale(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5, 6], widget=widgets.RadioSelect)


def make_6_point_likert_skale_horizontal(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5, 6], widget=widgets.RadioSelectHorizontal)


class Player(BasePlayer):
    age = models.IntegerField(
        label='What is your age?',
        min=18,
        max=95,
        error_messages={
            'min_value': 'Please enter an age of at least 18.',
            'max_value': 'Please enter an age of 99 or less.',
            'invalid': 'Please enter a valid age between 18 and 95.',
        }
    )

    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Transgender', 'Transgender'], ['Non-binary', 'Non-binary'],
                 ['Prefer not to say', 'Prefer not to say']],
        label='Which gender do you identify with?',
        widget=widgets.RadioSelect)


    # field_of_study = models.StringField(
    #     choices=[
    #         ['Economics', 'Economics'],
    #         ['Engineering, Science, Mathematics, Information Systems or Computer Science',
    #          'Engineering, Science, Mathematics, Information Systems or Computer Science'],
    #         ['Natural Science (e.g. Physics, Biology etc.)', 'Natural Science (e.g. Physics, Biology etc.)'],
    #         ['Humanities, Social Sciences or Psychology', 'Humanities, Social Sciences or Psychology'],
    #         ['Others', 'Others']
    #     ],
    #     label='What is your field of study?',
    #     widget=widgets.RadioSelect
    # )

    prior_experience = models.IntegerField(
        choices=[
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [5, '5'],
            [6, '6']
        ],
        label='Please rate your prior experience in virtual collaboration: '
              'On a scale from 1 (Novice) to 6 (Expert) ',
        widget=widgets.RadioSelectHorizontal
    )

    frequency_of_usage = models.StringField(
        choices=[
            ['At least 1 day in a week', 'At least 1 day in a week'],
            ['At least 2 days in a week', 'At least 2 days in a week'],
            ['At least 3 days in a week', 'At least 3 days in a week'],
            ['At least 4 days in a week', 'At least 4 days in a week'],
            ['5 days in a week or more', '5 days in a week or more']
        ],
        label='Please indicate your frequency of usage of video meetings in an average week',
        widget=widgets.RadioSelect
    )

    # video meeting preferences # TODO
    vm_universalism_nature = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_benevolence_caring = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_benevolence_dependability = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_selfdirection_thought = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_selfdirection_action = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_hedonism = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_power_resources = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_security_personal = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_security_societal = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_tradition = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_conformity_interpersonal = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_humility = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )
    vm_stimulation = make_6_point_likert_skale_horizontal(
        'In video meetings, ..'
    )

    # Portrait Value Questionnaire
    q1 = make_6_point_likert_skale('It is important to him/her to form his/her views independently.')
    q2 = make_6_point_likert_skale('It is important to him/her that his/her country is secure and stable.')
    q3 = make_6_point_likert_skale('It is important to him/her to have a good timeslots.')
    q4 = make_6_point_likert_skale('It is important to him/her to avoid upsetting other people.')
    q5 = make_6_point_likert_skale('It is important to him/her that the weak and vulnerable in society be protected.')
    q6 = make_6_point_likert_skale('It is important to him/her that people do what he/she says they should.')
    q7 = make_6_point_likert_skale('It is important to him/her never to think he/she deserves more than other people.')
    q8 = make_6_point_likert_skale('It is important to him/her to care for nature.')
    q9 = make_6_point_likert_skale('It is important to him/her that no one should ever shame him/her.')
    q10 = make_6_point_likert_skale('It is important to him/her always to look for different things to do.')
    q11 = make_6_point_likert_skale('It is important to him/her to take care of people he/she is close to.')
    q12 = make_6_point_likert_skale('It is important to him/her to have the power that money can bring.')
    q13 = make_6_point_likert_skale('It is very important to him/her to avoid disease and protect his/her health.')
    q14 = make_6_point_likert_skale('It is important to him/her to be tolerant toward all kinds of people and groups.')
    q15 = make_6_point_likert_skale('It is important to him/her never to violate rules or regulations.')
    q16 = make_6_point_likert_skale('It is important to him/her to make his/her own decisions about his/her life.')
    q17 = make_6_point_likert_skale('It is important to him/her to have ambitions in life.')
    q18 = make_6_point_likert_skale('It is important to him/her to maintain traditional values and ways of thinking.')
    q19 = make_6_point_likert_skale('It is important to him/her that people he/she knows have full confidence in him/her.')
    q20 = make_6_point_likert_skale('It is important to him/her to be wealthy.')
    q21 = make_6_point_likert_skale('It is important to him/her to take part in activities to defend nature.')
    q22 = make_6_point_likert_skale('It is important to him/her never to annoy anyone.')
    q23 = make_6_point_likert_skale('It is important to him/her to develop his/her own opinions.')
    q24 = make_6_point_likert_skale('It is important to him/her to protect his/her public image.')
    q25 = make_6_point_likert_skale('It is very important to him/her to help the people dear to him/her.')
    q26 = make_6_point_likert_skale('It is important to him/her to be personally safe and secure.')
    q27 = make_6_point_likert_skale('It is important to him/her to be a dependable and trustworthy friend.')
    q28 = make_6_point_likert_skale('It is important to him/her to take risks that make life exciting.')
    q29 = make_6_point_likert_skale('It is important to him/her to have the power to make people do what he/she wants.')
    q30 = make_6_point_likert_skale('It is important to him/her to plan his/her activities independently.')
    q31 = make_6_point_likert_skale('It is important to him/her to follow rules even when no one is watching.')
    q32 = make_6_point_likert_skale('It is important to him/her to be very successful.')
    q33 = make_6_point_likert_skale('It is important to him/her to follow his/her family’s customs or the customs of a religion.')
    q34 = make_6_point_likert_skale('It is important to him/her to listen to and understand people who are different from him/her.')
    q35 = make_6_point_likert_skale('It is important to him/her to have a strong state that can defend its citizens.')
    q36 = make_6_point_likert_skale('It is important to him/her to enjoy life’s pleasures.')
    q37 = make_6_point_likert_skale('It is important to him/her that every person in the world have equal opportunities in life.')
    q38 = make_6_point_likert_skale('It is important to him/her to be humble.')
    q39 = make_6_point_likert_skale('It is important to him/her to figure things out himself/herself.')
    q40 = make_6_point_likert_skale('It is important to him/her to honor the traditional practices of his/her culture.')
    q41 = make_6_point_likert_skale('It is important to him/her to be the one who tells others what to do.')
    q42 = make_6_point_likert_skale('It is important to him/her to obey all the laws.')
    q43 = make_6_point_likert_skale('It is important to him/her to have all sorts of new experiences.')
    q44 = make_6_point_likert_skale('It is important to him/her to own expensive things that show his/her wealth.')
    q45 = make_6_point_likert_skale('It is important to him/her to protect the natural environment from destruction or pollution.')
    q46 = make_6_point_likert_skale('It is important to him/her to take advantage of every opportunity to have fun.')
    q47 = make_6_point_likert_skale('It is important to him/her to concern himself/herself with every need of his/her dear ones.')
    q48 = make_6_point_likert_skale('It is important to him/her that people recognize what he/she achieves.')
    q49 = make_6_point_likert_skale('It is important to him/her never to be humiliated.')
    q50 = make_6_point_likert_skale('It is important to him/her that his/her country protect itself against all threats.')
    q51 = make_6_point_likert_skale('It is important to him/her never to make other people angry.')
    q52 = make_6_point_likert_skale('It is important to him/her that everyone be treated justly, even people he/she doesn’t know.')
    q53 = make_6_point_likert_skale('It is important to him/her to avoid anything dangerous.')
    q54 = make_6_point_likert_skale('It is important to him/her to be satisfied with what he/she has and not ask for more.')
    q55 = make_6_point_likert_skale('It is important to him/her that all his/her friends and family can rely on him/her completely.')
    q56 = make_6_point_likert_skale('It is important to him/her to be free to choose what he/she does by himself/herself.')
    q57 = make_6_point_likert_skale('It is important to him/her to accept people even when he/she disagrees with them.')

    # attention checks
    attention_check = models.IntegerField(initial=0)  # used to count attention checks
    attention_vm = make_6_point_likert_skale_horizontal('In video meetings, I would answer this attention check with the second option from the right to indicate that I answere these questions attentively')
    attention1 = make_6_point_likert_skale(
        'It is important to him/her to select the option "Not like me at all " to show that he/she is answering the questions attentively.')
    attention2 = make_6_point_likert_skale(
        'It is important to him/her to select the option "Not like me " to show that he/she is answering the questions attentively.')
    attention3 = make_6_point_likert_skale(
        'It is important to him/her to select the option "A little like me " to show that he/she is answering the questions attentively.')

    # Computed subscale scores
    universalism_nature = models.FloatField()  # Universalism-Nature: Preservation of the natural environment
    universalism_concern = models.FloatField()  # Universalism-Concern: Commitment to equality, justice, and protection for all people
    universalism_tolerance = models.FloatField()  # Universalism-Tolerance: Acceptance and understanding of those who are different from oneself
    benevolence_caring = models.FloatField()  # Benevolence-Caring: Devotion to the welfare of in-group members
    benevolence_dependability = models.FloatField()  # Benevolence-Dependability: Being a reliable and trustworthy member of the in-group
    selfdirection_thought = models.FloatField()  # Self-Direction-Thought: The freedom to cultivate one’s own ideas and abilities
    selfdirection_action = models.FloatField()  # Self-Direction-Action: The freedom to determine one’s own actions
    hedonism = models.FloatField()  # Hedonism: Definition unchanged
    achievement = models.FloatField()  # Achievement: Definition unchanged
    power_dominance = models.FloatField()  # Power-Dominance: Power through exercising control over people
    power_resources = models.FloatField()  # Power-Resources: Power through control of material and social resources
    face = models.FloatField()  # Face: Security and power through maintaining one’s public image and avoiding humiliation
    security_personal = models.FloatField()  # Security-Personal: Safety in one’s immediate environment
    security_societal = models.FloatField()  # Security-Societal: Safety and stability in the wider society
    tradition = models.FloatField()  # Tradition: Maintaining and preserving cultural, family, or religious traditions
    conformity_rules = models.FloatField()  # Conformity-Rules: Compliance with rules, laws, and formal obligations
    conformity_interpersonal = models.FloatField()  # Conformity-Interpersonal: Avoidance of upsetting or harming other people
    humility = models.FloatField()  # Humility: Recognizing one’s insignificance in the larger scheme of things
    stimulation = models.FloatField()

    # payoff
    total_payoff = models.FloatField()
    additional_payoff = models.FloatField()
    svo_payoff = models.FloatField()
    wlg_payoff = models.FloatField()
    attention_fail_cost = models.FloatField()
    final_payoff = models.FloatField()


# PAGES
class Demographics(Page):
    """  Questionnaire for Demographics"""
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   # 'field_of_study',
                   'prior_experience',
                   'frequency_of_usage']

    def error_message(self, values):
        # Custom validation for age field
        age = values.get('age')
        if age is not None:
            if age < 18:
                return 'Please enter an age of at least 18.'
            elif age > 95:
                return 'Please enter an age of 95 or less.'


class VideoMeetingBehaviorII(Page):
    form_model = 'player'
    form_fields = ['vm_universalism_nature', 'vm_benevolence_caring', 'vm_benevolence_dependability',
                   'vm_selfdirection_thought', 'vm_selfdirection_action', 'attention_vm', 'vm_hedonism',
                   'vm_power_resources', 'vm_security_personal', 'vm_security_societal', 'vm_tradition',
                   'vm_conformity_interpersonal', 'vm_humility', 'vm_stimulation']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention_vm != 5:
            player.attention_check += 1


class IntroPVQ(Page):
    form_model = 'player'


class SurveyPVQ1(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']


class SurveyPVQ2(Page):
    form_model = 'player'
    form_fields = ['q11', 'q12', 'q13', 'q14', 'attention1', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention1 != 1:
            player.attention_check += 1


class SurveyPVQ3(Page):
    form_model = 'player'
    form_fields = ['q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30']


class SurveyPVQ4(Page):
    form_model = 'player'
    form_fields = ['q31', 'q32', 'q33', 'q34', 'attention2', 'q35', 'q36', 'q37', 'q38', 'q39', 'q40']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention2 != 2:
            player.attention_check += 1


class SurveyPVQ5(Page):
    form_model = 'player'
    form_fields = ['q41', 'q42', 'q43', 'q44', 'q45', 'attention3', 'q46', 'q47', 'q48', 'q49', 'q50']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.attention3 != 3:
            player.attention_check += 1


class SurveyPVQ6(Page):
    form_model = 'player'
    form_fields = ['q51', 'q52', 'q53', 'q54', 'q55', 'q56', 'q57']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        # pvq construct calculation
        player.universalism_nature = pvq_scale_calc(player.q8, player.q21, player.q45)
        player.universalism_concern = pvq_scale_calc(player.q5, player.q37, player.q52)
        player.universalism_tolerance = pvq_scale_calc(player.q14, player.q34, player.q57)
        player.benevolence_caring = pvq_scale_calc(player.q11, player.q25, player.q47)
        player.benevolence_dependability = pvq_scale_calc(player.q19, player.q27, player.q55)
        player.selfdirection_thought = pvq_scale_calc(player.q1, player.q23, player.q39)
        player.selfdirection_action = pvq_scale_calc(player.q16, player.q30, player.q56)
        player.hedonism = pvq_scale_calc(player.q3, player.q36, player.q46)
        player.achievement = pvq_scale_calc(player.q17, player.q32, player.q48)
        player.power_dominance = pvq_scale_calc(player.q6, player.q29, player.q41)
        player.power_resources = pvq_scale_calc(player.q12, player.q20, player.q44)
        player.face = pvq_scale_calc(player.q9, player.q24, player.q49)
        player.security_personal = pvq_scale_calc(player.q13, player.q26, player.q53)
        player.security_societal = pvq_scale_calc(player.q2, player.q35, player.q50)
        player.tradition = pvq_scale_calc(player.q18, player.q33, player.q40)
        player.conformity_rules = pvq_scale_calc(player.q15, player.q31, player.q42)
        player.conformity_interpersonal = pvq_scale_calc(player.q4, player.q22, player.q51)
        player.humility = pvq_scale_calc(player.q7, player.q38, player.q54)
        player.stimulation = pvq_scale_calc(player.q10, player.q28, player.q43)

        # payoff calculation
        if player.participant.svo_other:
            # if a team could form, take the svo self, svo other and WLG payout
            player.additional_payoff = (player.participant.svo_self
                                              + player.participant.svo_other
                                              + player.participant.wlg_payoff)

        else:
            # if no team could form, compensate by 2 times svo self and 200 ECU
            player.additional_payoff = (player.participant.svo_self * 2) + 200

        player.participant.additional_payoff = round(player.additional_payoff, 2)
        player.participant.fixed_payoff = C.FIX_PAYOFF
        player.total_payoff = C.FIX_PAYOFF + player.additional_payoff
        player.participant.total_payoff = player.total_payoff
        print(player.total_payoff)
        player.participant.attention_fail = player.attention_check
        player.attention_fail_cost = round(1 - (player.attention_check / 5), 2)  # reduce payout up 80 % (20 % per failed attention check)
        player.participant.attention_fail_cost = player.attention_fail_cost
        player.final_payoff = player.total_payoff * player.attention_fail_cost
        player.participant.final_payoff = round(player.final_payoff, 2)


page_sequence = [
    VideoMeetingBehaviorII,
    IntroPVQ,
    SurveyPVQ1,
    SurveyPVQ2,
    SurveyPVQ3,
    SurveyPVQ4,
    SurveyPVQ5,
    SurveyPVQ6,
    Demographics,
]
