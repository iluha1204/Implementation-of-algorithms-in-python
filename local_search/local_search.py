import numpy as np
import os
from random import *
import xlsxwriter
# import itertools
import time
import datetime
import bisect

XLSX_FILE_NAME_WITH_PATH = os.path.dirname(__file__) + r'/' + 'inputs_results_temp.xlsx'

FILE_WITH_INPUTS = os.path.dirname(__file__) + r'/' + 'inputs_numbered.txt'
now = datetime.datetime.now()
file_name = str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '_' + str(now.minute) + '_' + str(now.second) + '.txt'
FILE_NAME_WITH_PATH_SAVE = os.path.dirname(__file__) + r'/' + str(file_name)

NUMBER_OF_JOBS = 25
NUMBER_OF_MACHINES = 6
K_NUMBER = None
WRITE_TEXT_TO_FILE = False
BIG_INPUT = True

def getJobsAsList():
    jobs = []
    index = 1
    for i in range(1, NUMBER_OF_JOBS + 1):
        bisect.insort(jobs, {'index': index, 'time': i*i}, key=lambda job: -1 * job['time'])
        index += 1

    # jobsAsString = '[234(1), 228(2), 222(3), 234(4), 228(5), 241(6), 253(7), 228(8), 252(9), 235(10), 260(11), 250(12), 234(13), 245(14), 226(15), 231(16), 227(17), 249(18), 235(19), 222(20), 228(21), 227(22), 228(23), 227(24), 225(25), 222(26), 255(27), 256(28), 246(29), 244(30), 230(31), 225(32), 223(33), 224(34), 236(35), 243(36), 239(37), 249(38), 242(39), 256(40), 251(41), 250(42), 229(43), 240(44), 242(45), 236(46), 247(47), 223(48), 253(49), 228(50), 258(51), 235(52), 255(53), 260(54), 227(55), 257(56), 260(57), 254(58), 244(59), 224(60), 238(61), 253(62), 228(63), 256(64), 245(65), 221(66), 233(67), 237(68), 237(69), 244(70), 234(71), 223(72), 236(73), 231(74), 257(75), 260(76), 237(77), 242(78), 232(79), 221(80), 241(81), 229(82), 228(83), 234(84), 228(85), 226(86), 238(87), 236(88), 229(89), 248(90), 242(91), 235(92), 257(93), 247(94), 233(95), 254(96), 225(97), 243(98), 229(99), 256(100), 233(101), 221(102), 223(103), 230(104), 257(105), 237(106), 225(107), 254(108), 251(109), 233(110), 236(111), 221(112), 259(113), 246(114), 247(115), 259(116), 250(117), 232(118), 247(119), 223(120), 245(121), 223(122), 238(123), 256(124), 239(125), 230(126), 233(127), 252(128), 257(129), 238(130), 224(131), 248(132), 228(133), 237(134), 221(135), 221(136), 235(137), 236(138), 247(139), 233(140), 225(141), 232(142), 224(143), 238(144), 240(145), 251(146), 229(147), 254(148), 254(149), 236(150), 240(151), 260(152), 247(153), 247(154), 234(155), 259(156), 235(157), 233(158), 226(159), 243(160), 238(161), 245(162), 244(163), 239(164), 254(165), 225(166), 259(167), 254(168), 244(169), 233(170), 230(171), 224(172), 237(173), 242(174), 260(175), 224(176), 257(177), 251(178), 229(179), 228(180), 226(181), 259(182), 231(183), 243(184), 230(185), 246(186), 245(187), 252(188), 241(189), 235(190), 225(191), 258(192), 259(193), 251(194), 254(195), 221(196), 223(197), 226(198), 231(199), 243(200), 245(201), 247(202), 259(203), 246(204), 254(205), 252(206), 248(207), 246(208), 239(209), 237(210), 237(211), 260(212), 248(213), 255(214), 244(215), 225(216), 221(217), 259(218), 238(219), 230(220), 231(221), 237(222), 247(223), 260(224), 231(225), 247(226), 231(227), 251(228), 258(229), 252(230), 254(231), 236(232), 247(233), 254(234), 224(235), 248(236), 239(237), 223(238), 248(239), 247(240), 251(241), 228(242), 227(243), 235(244), 247(245), 226(246), 257(247), 246(248), 222(249), 256(250), 253(251), 250(252), 246(253), 230(254), 236(255), 230(256), 246(257), 232(258), 245(259), 223(260), 247(261), 237(262), 242(263), 246(264), 237(265), 235(266), 234(267), 248(268), 231(269), 234(270), 233(271), 231(272), 231(273), 232(274), 256(275), 257(276), 226(277), 242(278), 251(279), 252(280), 227(281), 256(282), 260(283), 233(284), 227(285), 222(286), 260(287), 227(288), 227(289), 230(290), 242(291), 232(292), 230(293), 237(294), 252(295), 257(296), 234(297), 241(298), 234(299), 253(300), 251(301), 243(302), 254(303), 248(304), 232(305), 223(306), 256(307), 246(308), 260(309), 232(310), 225(311), 258(312), 241(313), 250(314), 239(315), 253(316), 234(317), 258(318), 257(319), 240(320), 232(321), 221(322), 233(323), 251(324), 231(325), 256(326), 222(327), 230(328), 230(329), 236(330), 228(331), 249(332), 252(333), 231(334), 256(335), 235(336), 224(337), 256(338), 228(339), 242(340), 239(341), 242(342), 226(343), 259(344), 224(345), 232(346), 235(347), 253(348), 231(349), 230(350), 228(351), 229(352), 243(353), 247(354), 244(355), 236(356), 255(357), 243(358), 233(359), 231(360), 223(361), 240(362), 244(363), 223(364), 257(365), 228(366), 245(367), 244(368), 256(369), 246(370), 229(371), 238(372), 240(373), 256(374), 233(375), 258(376), 226(377), 221(378), 253(379), 221(380), 232(381), 241(382), 243(383), 237(384), 225(385), 253(386), 238(387), 233(388), 229(389), 222(390), 243(391), 259(392), 229(393), 226(394), 229(395), 230(396), 250(397), 246(398), 250(399), 239(400), 244(401), 247(402), 234(403), 234(404), 260(405), 252(406), 232(407), 249(408), 227(409), 227(410), 232(411), 253(412), 226(413), 226(414), 230(415), 250(416), 223(417), 245(418), 259(419), 247(420), 229(421), 260(422), 232(423), 226(424), 229(425), 254(426), 235(427), 235(428), 237(429), 231(430), 252(431), 221(432), 233(433), 255(434), 222(435), 224(436), 245(437), 251(438), 228(439), 240(440), 260(441), 252(442), 238(443), 223(444), 225(445), 238(446), 221(447), 240(448), 247(449), 221(450), 251(451), 260(452), 244(453), 233(454), 246(455), 225(456), 240(457), 245(458), 223(459), 246(460), 223(461), 246(462), 253(463), 259(464), 249(465), 222(466), 237(467), 253(468), 246(469), 254(470), 259(471), 252(472), 229(473), 241(474), 245(475), 242(476), 251(477), 225(478), 254(479), 230(480), 223(481), 250(482), 259(483), 240(484), 257(485), 234(486), 254(487), 260(488), 224(489), 222(490), 227(491), 239(492), 225(493), 223(494), 248(495), 242(496), 245(497), 224(498), 260(499), 254(500), 239(501), 234(502), 224(503), 241(504), 233(505), 237(506), 232(507), 225(508), 259(509), 222(510), 234(511), 253(512), 241(513), 227(514), 242(515), 226(516), 232(517), 249(518), 259(519), 222(520), 250(521), 256(522), 230(523), 244(524), 259(525), 232(526), 247(527), 254(528), 226(529), 230(530), 222(531), 240(532), 228(533), 238(534), 239(535), 231(536), 222(537), 233(538), 242(539), 227(540), 260(541), 247(542), 229(543), 235(544), 237(545), 224(546), 231(547), 250(548), 246(549), 233(550), 245(551), 252(552), 243(553), 243(554), 254(555), 225(556), 241(557), 249(558), 239(559), 245(560), 253(561), 242(562), 238(563), 239(564), 224(565), 235(566), 226(567), 224(568), 260(569), 243(570), 234(571), 241(572), 229(573), 247(574), 242(575), 230(576), 242(577), 252(578), 230(579), 246(580), 259(581), 239(582), 237(583), 233(584), 257(585), 231(586), 239(587), 236(588), 235(589), 253(590), 250(591), 253(592), 257(593), 235(594), 245(595), 225(596), 237(597), 223(598), 231(599), 249(600), 223(601), 223(602), 247(603), 228(604), 232(605), 223(606), 252(607), 225(608), 256(609), 254(610), 237(611), 252(612), 239(613), 235(614), 222(615), 225(616), 221(617), 237(618), 221(619), 253(620), 251(621), 246(622), 229(623), 233(624), 236(625), 259(626), 242(627), 244(628), 260(629), 232(630), 251(631), 259(632), 242(633), 255(634), 238(635), 228(636), 247(637), 245(638), 247(639), 225(640), 234(641), 236(642), 231(643), 246(644), 242(645), 232(646), 252(647), 245(648), 244(649), 230(650), 221(651), 235(652), 255(653), 222(654), 241(655), 239(656), 228(657), 221(658), 237(659), 224(660), 226(661), 232(662), 247(663), 223(664), 252(665), 244(666), 238(667), 230(668), 252(669), 241(670), 260(671), 255(672), 259(673), 226(674), 227(675), 248(676), 254(677), 237(678), 240(679), 227(680), 257(681), 241(682), 234(683), 259(684), 246(685), 238(686), 226(687), 230(688), 231(689), 226(690), 255(691), 238(692), 228(693), 239(694), 229(695), 232(696), 250(697), 251(698), 248(699), 228(700), 255(701), 241(702), 251(703), 254(704), 237(705), 248(706), 249(707), 245(708), 242(709), 232(710), 230(711), 245(712), 256(713), 259(714), 258(715), 238(716), 233(717), 257(718), 226(719), 257(720), 230(721), 249(722), 242(723), 247(724), 240(725), 243(726), 225(727), 240(728), 258(729), 254(730), 242(731), 237(732), 252(733), 241(734), 244(735), 246(736), 252(737), 253(738), 256(739), 225(740), 234(741), 222(742), 253(743), 241(744), 251(745), 256(746), 232(747), 252(748), 245(749), 222(750), 236(751), 249(752), 252(753), 246(754), 259(755), 251(756), 224(757), 223(758), 257(759), 239(760), 251(761), 246(762), 234(763), 225(764), 256(765), 252(766), 260(767), 250(768), 230(769), 256(770), 251(771), 231(772), 222(773), 232(774), 244(775), 253(776), 254(777), 228(778), 238(779), 221(780), 236(781), 228(782), 224(783), 227(784), 235(785), 258(786), 222(787), 227(788), 249(789), 228(790), 225(791), 227(792), 234(793), 221(794), 254(795), 224(796), 227(797), 255(798), 246(799), 224(800), 255(801), 239(802), 236(803), 252(804), 251(805), 257(806), 239(807), 243(808), 232(809), 226(810), 254(811), 254(812), 253(813), 251(814), 252(815), 248(816), 256(817), 232(818), 232(819), 235(820), 234(821), 234(822), 255(823), 235(824), 260(825), 253(826), 236(827), 249(828), 237(829), 258(830), 258(831), 237(832), 245(833), 230(834), 243(835), 230(836), 242(837), 230(838), 235(839), 246(840), 241(841), 221(842), 225(843), 230(844), 232(845), 247(846), 254(847), 232(848), 252(849), 260(850), 243(851), 234(852), 234(853), 230(854), 251(855), 222(856), 260(857), 253(858), 254(859), 257(860), 222(861), 227(862), 258(863), 223(864), 229(865), 233(866), 222(867), 254(868), 251(869), 256(870), 234(871), 259(872), 253(873), 250(874), 230(875), 224(876), 221(877), 249(878), 248(879), 249(880), 224(881), 223(882), 241(883), 230(884), 256(885), 245(886), 236(887), 221(888), 246(889), 235(890)]'
    # jobs = getJobsAsListFromString(jobsAsString)
    return jobs

def getJobsAsListFromString(jobsAsString: str):
    jobsForReturn = []
    jobsAsString = jobsAsString.replace('[', '')
    jobsAsString = jobsAsString.replace(']', '')
    jobsAsList = jobsAsString.split(',')
    for jobAsString in jobsAsList:
        job_index = int(jobAsString.split('(')[1].replace(')', ''))
        job_time = int(jobAsString.split('(')[0])
        bisect.insort(jobsForReturn, {'index': job_index, 'time': job_time}, key=lambda job: -1 * job['time'])
    return jobsForReturn

def getNewFreeSystem(number_of_machines):
    system = {'machines' : [], 'maxspan' : 0, 'opt_maxspan' : 0, 'number_of_jobs' : 0, 'sum_of_jobs_times' : 0}
    for j in range(1, number_of_machines+1):
        system['machines'].append({"jobs" : [], 'jobs_count': 0, "span" : 0, 'index': j})
    return system

def getSystem(input):
    jobs = getJobsAsListFromString(input['jobs_string'])
    system = getNewFreeSystem(input['number_of_machines'])
    for job in jobs:
        system['sum_of_jobs_times'] += job['time']
        system['number_of_jobs'] += 1
    makeStartingPosition(system, jobs)
    system['maxspan'] = getMaxspan(system)
    system['opt_maxspan'] = int(np.ceil(system['sum_of_jobs_times']/(input['number_of_machines'])))
    return system

def makeStartingPosition(system, jobs):

    # # All jobs on machine #1
    # for machine in system['machines']:
    #     if machine['index'] == 1:
    #         machine['jobs'] = jobs
    #         for job in machine['jobs']:
    #             machine['span'] += job['time']
    #             machine['jobs_count'] += 1

    # # Separate jobs on all machines
    # step_count = 0
    # is_solution_found = False
    # while not is_solution_found:
    #     if step_count < K_NUMBER:
    #         for machine in system['machines']:
    #             try:
    #                 addJobToMachine(jobs[0], machine)
    #             except:
    #                 is_solution_found = True
    #                 break
    #             jobs.remove(jobs[0])
    #         step_count += 1
    #     else:
    #         for machine in system['machines']:
    #             if machine['index'] == 1:
    #                 for job in jobs:
    #                     addJobToMachine(job, machine)
    #                 is_solution_found = True

    # LPT
    while True:
        if len(jobs) == 0:
            break
        for machine in reversed(system['machines']):
            if isMachineHaveFreeSpace(machine):
                addJobToMachine(jobs[0], machine)
                jobs.remove(jobs[0])
                break
        sortMachinesInSystemViaSpan(system, isReversed=True)

def getMaxspan(system):
    maxspan = 0
    for machine in system['machines']:
        if maxspan < machine['span']:
            maxspan = machine['span']
    return maxspan

def getJobsAsString(jobs):
    jobs_as_string = '['
    is_first_job = True
    for job in jobs:
        if is_first_job:
            jobs_as_string += str(job['time']) + '(' + str(job['index']) + ')'
            is_first_job = False
        else:
            jobs_as_string += ', ' + str(job['time']) + '(' + str(job['index']) + ')'
    if jobs_as_string == '[':
        jobs_as_string += 'No jobs'
    jobs_as_string += ']'
    return jobs_as_string

# def getSumOfAllTimesOfJobs(jobs):
#     sum = 0
#     for job in jobs:
#         sum += job['time']
#     return sum

def getJobsFromMachinesToArray(system):
    jobs = []
    for machine in system['machines']:
        for job in machine['jobs']:
            jobs.append(job)
    jobs.sort(key=lambda job: job.get('index'))
    return jobs

def getBeautifullPrint(system):
    sortMachinesInSystemViaIndex(system, isReversed = False)
    text = 'Maxspan: ' + str(system['maxspan']) + '\n' + \
        '******************\n'
    for machine in system['machines']:
        text += ('Machine #' + str(machine['index']) + ': ' + getJobsAsString(machine['jobs']) + '; Jobs: ' + str(len(machine['jobs'])) + '; Time: ' + str(machine['span'])) + '\n'
    text += '################################\n'
    print(text)
    if WRITE_TEXT_TO_FILE:
        with open(FILE_NAME_WITH_PATH_SAVE, 'a') as f:
            f.write(text + '\n')

def findIndexOfMostLoadedMachine(system):
    system['machines'].sort(key=lambda machine: machine.get('span'), reverse = True)
    return system['machines'][0]['index']

def findIndexOfLeastLoadedMachine(system):
    system['machines'].sort(key=lambda machine: machine.get('span'), reverse = False)
    return system['machines'][0]['index']

def isMachineHaveFreeSpace(machine):
    if machine['jobs_count'] < K_NUMBER or machine['index'] == 1:
        return True
    else:
        return False

# def sortJobsOnAllMachines(system, isReversed = False):
#         for machine in system['machines']:
#             machine['jobs'].sort(key=lambda job: job.get('time'), reverse = isReversed)

def sortMachinesInSystemViaSpan(system, isReversed = False):
        system['machines'].sort(key=lambda machine: machine.get('span'), reverse = isReversed)

def sortMachinesInSystemViaIndex(system, isReversed = False):
        system['machines'].sort(key=lambda machine: machine.get('index'), reverse = isReversed)

def addJobToMachine(job, machine):
    bisect.insort(machine['jobs'], job, key=lambda job: -1 * job['time'])
    machine['span'] += job['time']
    machine['jobs_count'] += 1

def removeJobFromMachine(job, machine):
    machine['jobs'].remove(job)
    machine['span'] -= job['time']
    machine['jobs_count'] -= 1

def removeJobFromMachineAndAddToAnother(job, machine_remove, machine_add):
    removeJobFromMachine(job, machine_remove)
    addJobToMachine(job, machine_add)

def doFisrtStep(system, number_of_steps):
    for machine_1 in system['machines']:
            for machine_2 in reversed(system['machines']):
                if machine_1['index'] == machine_2['index'] or not isMachineHaveFreeSpace(machine_2):
                    continue
                current_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
                for job_1 in machine_1['jobs']:
                    removeJobFromMachineAndAddToAnother(job_1, machine_1, machine_2)
                    new_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
                    if new_maxspan_of_machines < current_maxspan_of_machines:
                        system['maxspan'] = getMaxspan(system)

                        if not BIG_INPUT:
                            text = '################################\n' + 'Step Number #' + str(number_of_steps) + ': '
                            text += "Job " + str(job_1['time']) + '(' + str(job_1['index']) + ') from machine #' + str(machine_1['index']) + ' has been moved to machine #' + str(machine_2['index']) + '.'
                            print(text)
                            if WRITE_TEXT_TO_FILE:
                                with open(FILE_NAME_WITH_PATH_SAVE, 'a') as f:
                                        f.write(text + '\n')
                            getBeautifullPrint(system)

                        return True
                    removeJobFromMachineAndAddToAnother(job_1, machine_2, machine_1)
    return False

def doSecondStep(system, number_of_steps):
    for machine_1 in system['machines']:
        for machine_2 in reversed(system['machines']):
            if machine_1['index'] == machine_2['index']:
                continue
            current_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
            for job_from_machine_1 in machine_1['jobs']:
                for job_from_machine_2 in machine_2['jobs']:
                    removeJobFromMachineAndAddToAnother(job_from_machine_1, machine_1, machine_2)
                    removeJobFromMachineAndAddToAnother(job_from_machine_2, machine_2, machine_1)
                    new_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
                    if new_maxspan_of_machines < current_maxspan_of_machines:
                        system['maxspan'] = getMaxspan(system)

                        if not BIG_INPUT:
                            text = '################################\n' + 'Step Number #' + str(number_of_steps) + ': '
                            text += "Job " + str(job_from_machine_1['time']) + '(' + str(job_from_machine_1['index']) + ') from machine #' + str(machine_1['index']) + \
                                        ' and job ' + str(job_from_machine_2['time']) + '(' + str(job_from_machine_2['index']) + ') from machine #' + str(machine_2['index']) + ' switched places.'
                            print(text)
                            if WRITE_TEXT_TO_FILE:
                                with open(FILE_NAME_WITH_PATH_SAVE, 'a') as f:
                                        f.write(text + '\n')
                            getBeautifullPrint(system)

                        return True
                    else:
                        removeJobFromMachineAndAddToAnother(job_from_machine_1, machine_2, machine_1)
                        removeJobFromMachineAndAddToAnother(job_from_machine_2, machine_1, machine_2)
    return False

def doThirdStep(system, number_of_steps):
    for machine_1 in system['machines']:
        for machine_2 in reversed(system['machines']):
            if machine_1['index'] == machine_2['index'] or not isMachineHaveFreeSpace(machine_2):
                continue
            current_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
            for job_1_from_machine_1 in machine_1['jobs']:
                for job_2_from_machine_1 in machine_1['jobs']:
                    if job_2_from_machine_1['index'] == job_1_from_machine_1['index']:
                        continue
                    for job_from_machine_2 in machine_2['jobs']:
                        removeJobFromMachineAndAddToAnother(job_1_from_machine_1, machine_1, machine_2)
                        removeJobFromMachineAndAddToAnother(job_2_from_machine_1, machine_1, machine_2)
                        removeJobFromMachineAndAddToAnother(job_from_machine_2, machine_2, machine_1)
                        new_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
                        if new_maxspan_of_machines < current_maxspan_of_machines:
                            system['maxspan'] = getMaxspan(system)

                            if not BIG_INPUT:
                                text = '################################\n' + 'Step Number #' + str(number_of_steps) + ': '
                                text += "Jobs " + str(job_1_from_machine_1['time']) + '(' + str(job_1_from_machine_1['index']) + ') and ' + str(job_2_from_machine_1['time']) + '(' + str(job_2_from_machine_1['index']) + ') from machine #' + str(machine_1['index']) + \
                                            ' switched places with job ' + str(job_from_machine_2['time']) + '(' + str(job_from_machine_2['index']) + ') from machine #' + str(machine_2['index']) + '.'
                                print(text)
                                if WRITE_TEXT_TO_FILE:
                                    with open(FILE_NAME_WITH_PATH_SAVE, 'a') as f:
                                            f.write(text + '\n')
                                getBeautifullPrint(system)

                            return True
                        else:
                            removeJobFromMachineAndAddToAnother(job_1_from_machine_1, machine_2, machine_1)
                            removeJobFromMachineAndAddToAnother(job_2_from_machine_1, machine_2, machine_1)
                            removeJobFromMachineAndAddToAnother(job_from_machine_2, machine_1, machine_2)
    return False

def doFourthStep(system, number_of_steps):
    for machine_1 in system['machines']:
        for machine_2 in reversed(system['machines']):
            if machine_1['index'] == machine_2['index']:
                continue
            current_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
            for job_1_from_machine_1 in machine_1['jobs']:
                for job_2_from_machine_1 in machine_1['jobs']:
                    if job_2_from_machine_1['index'] == job_1_from_machine_1['index']:
                        continue
                    for job_1_from_machine_2 in machine_2['jobs']:
                        for job_2_from_machine_2 in machine_2['jobs']:
                            if job_2_from_machine_2['index'] == job_1_from_machine_2['index']:
                                continue
                            removeJobFromMachineAndAddToAnother(job_1_from_machine_1, machine_1, machine_2)
                            removeJobFromMachineAndAddToAnother(job_2_from_machine_1, machine_1, machine_2)
                            removeJobFromMachineAndAddToAnother(job_1_from_machine_2, machine_2, machine_1)
                            removeJobFromMachineAndAddToAnother(job_2_from_machine_2, machine_2, machine_1)
                            new_maxspan_of_machines = max(machine_1['span'], machine_2['span'])
                            if new_maxspan_of_machines < current_maxspan_of_machines:
                                system['maxspan'] = getMaxspan(system)

                                if not BIG_INPUT:
                                    text = '################################\n' + 'Step Number #' + str(number_of_steps) + ': '
                                    text += "Jobs " + str(job_1_from_machine_1['time']) + '(' + str(job_1_from_machine_1['index']) + ') and ' + str(job_2_from_machine_1['time']) + '(' + str(job_2_from_machine_1['index']) + ') from machine #' + str(machine_1['index']) + \
                                                ' switched places with jobs ' + str(job_1_from_machine_2['time']) + '(' + str(job_1_from_machine_2['index']) + ') and ' + str(job_2_from_machine_2['time']) + '(' + str(job_2_from_machine_2['index']) + ') from machine #' + str(machine_2['index']) + '.'
                                    print(text)
                                    if WRITE_TEXT_TO_FILE:
                                        with open(FILE_NAME_WITH_PATH_SAVE, 'a') as f:
                                                f.write(text + '\n')
                                    getBeautifullPrint(system)

                                return True
                            else:
                                removeJobFromMachineAndAddToAnother(job_1_from_machine_1, machine_2, machine_1)
                                removeJobFromMachineAndAddToAnother(job_2_from_machine_1, machine_2, machine_1)
                                removeJobFromMachineAndAddToAnother(job_1_from_machine_2, machine_1, machine_2)
                                removeJobFromMachineAndAddToAnother(job_2_from_machine_2, machine_1, machine_2)
    return False

def printSystemInfoToFile(system):
    jobs = getJobsFromMachinesToArray(system)
    infoAsString = '************************************\n' + \
        'Number of jobs: ' + str(system['number_of_jobs']) + '\n' + \
        'Jobs (time(index)):\n' + getJobsAsString(jobs) + '\n' + \
        'Number of machines ' + str(len(system['machines'])) + '\n' + \
        'K number (allowed number of jobs on machine, except #1): ' + str(K_NUMBER) + '\n' + \
        'Sum of all times of jobs: ' + str(system['sum_of_jobs_times']) + '\n' + \
        'Optimal maxspan (if possible): ' + str(system['opt_maxspan']) + '\n' + \
        '************************************\n\n' + '################################\n' + 'Starting position'
    print(infoAsString)
    if WRITE_TEXT_TO_FILE:
        with open(FILE_NAME_WITH_PATH_SAVE, 'a') as f:
                f.write(infoAsString + '\n')

def getInputsFromFile():
    inputs = []
    with open(FILE_WITH_INPUTS, 'r') as f:
        file_text = f.read()
        index = 1
        while True:
            try:
                input = file_text.split(str(index)+'.')[1].split(str(index + 1)+'.')[0]
                inputs.append(input.strip())
                file_text = file_text.split(input)[1].strip()
                index += 1
            except:
                break
    inputs_objects = []
    for input in inputs:
        input_text = input
        jobs_string = input_text.split('Jobs (time(index)):')[1].split('Number of machines:')[0].strip()
        input_text = input_text.split(jobs_string)[1]
        number_of_machines = int(input_text.split('Number of machines:')[1].split('K number')[0].strip())
        input_text = input_text.split(f'Number of machines: {str(number_of_machines)}')[1]
        k_number = int(input_text.split('K number (allowed number of jobs on machine, except #1):')[1].strip())
        input_obj = {'jobs_string' : jobs_string, 'K' : k_number, 'number_of_machines' : number_of_machines}
        inputs_objects.append(input_obj)
    return inputs_objects

def updateXLSXFileWithResults(results):
    workbook = xlsxwriter.Workbook(XLSX_FILE_NAME_WITH_PATH)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Input Index')
    worksheet.write('B1', 'OPT maxspan (if possible)')
    worksheet.write('C1', 'Maxspan')
    worksheet.write('D1', 'Number of steps')
    worksheet.write('E1', 'Excecution time')
    for result in results:
        input_index = int(result['input_index'])
        row = input_index + 1
        worksheet.write('A' + str(row), input_index)
        worksheet.write('B' + str(row), result['opt_maxspan'])
        worksheet.write('C' + str(row), result['maxspan'])
        worksheet.write('D' + str(row), result['number_of_steps'])
        worksheet.write('E' + str(row), result['excecution_time'])
    workbook.close()

def main(input): 
    system = getSystem(input)
    is_solution_found = False
    number_of_steps = 0

    while not is_solution_found:
        if system['opt_maxspan'] == system['maxspan']:
            break
        sortMachinesInSystemViaSpan(system, isReversed = True)
        if doFisrtStep(system, number_of_steps):
            number_of_steps += 1
            continue
        if doSecondStep(system, number_of_steps):
            number_of_steps += 1
            continue
        if doThirdStep(system, number_of_steps):
            number_of_steps += 1
            continue
        if doFourthStep(system, number_of_steps):
            number_of_steps += 1
            continue
        is_solution_found = True
    return system['opt_maxspan'], system['maxspan'], number_of_steps

if __name__ == '__main__':
    results = []
    inputs_objects = getInputsFromFile()
    index_of_input = 0
    for input in inputs_objects:
        K_NUMBER = input['K']
        index_of_input += 1
        start_time = time.time()
        opt_maxspan, maxspan, number_of_steps = main(input)
        executuon_time = str(time.time() - start_time)
        if executuon_time == '0.0':
            executuon_time = '<0.0001'
        results.append({'opt_maxspan': opt_maxspan, 'maxspan': maxspan, 'number_of_steps': number_of_steps, 'excecution_time': executuon_time, 'input_index': index_of_input})
    updateXLSXFileWithResults(results)