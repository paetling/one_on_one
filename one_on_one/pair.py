from copy import deepcopy
import random

class Pair(object):
    @staticmethod
    def remove_excluded_people(group_dict, exclude_list):
        for person in exclude_list:
            for group, people in group_dict.iteritems():
                if person in people:
                    people.remove(person)

    def get_pairs(self, group_dict, exclude_list=[]):
        """
            This function is made to be subclassed. It takes
            in a dictionary with a structure described in Group.get().
            Exclude_list is a list of names that should not be included in the pairings
            It outputs a dictionary of the following format:
            {
                'pairs':  list of tuples. Each tuple contains 2 names who should
            be paired together for a meeting,
                'no_pair': If there is someone in your organization who could not be paired
            defaults to None if there is no such person
            }
        """
        raise NotImplementedError


class GCPair(Pair):
    @staticmethod
    def random_from_group_dict(group_dict, exclude_groups=[], exclude_people=[]):
        filtered_group_tuples = filter(lambda tup: tup[0] not in exclude_groups and len(tup[1]) > 0,
                                       map(lambda tup: (tup[0],
                                                      filter(lambda x: x not in exclude_people, tup[1])),
                                           group_dict.iteritems()))
        random_group_tuple = filtered_group_tuples[random.randint(0, len(filtered_group_tuples) - 1)]
        people = random_group_tuple[1]

        person = people[random.randint(0, len(people) - 1)]
        group_dict[random_group_tuple[0]].remove(person)
        return person

    @staticmethod
    def get_group_key_with_most_people(group_dict):
        max_key = ''
        max_length = 0
        for group_key, people in group_dict.iteritems():
            if len(people) > max_length:
                max_length = len(people)
                max_key = group_key
        return max_key

    @staticmethod
    def total_people(group_dict, exclude_groups=[]):
        if not group_dict:
            return 0
        return reduce(lambda x, y: x+y,
                      map(lambda tup: len(tup[1]),
                          filter(lambda tup: tup[0] not in exclude_groups,
                                 group_dict.iteritems())))

    @staticmethod
    def remove_all_empty_groups(group_dict):
        remove_keys = []
        for key in group_dict.keys():
            if len(group_dict[key]) == 0:
                remove_keys.append(key)
        for remove_key in remove_keys:
            del group_dict[remove_key]

    def get_pairs_not_your_group(self, group_dict, exclude_list=[]):
        """
            This function implements a random of grouping of people across teams. The algorithm
            is as follows:
                1. Take the group with the most people
                2. Randomly match each person in the group with someone in a different group
                3. Once this group is out of people, go back to step 1
                4. If you get to a situation at the end where one group still has people left,
                    randomly match those people to each other.
        """
        pairs = []
        left_over = None
        groups = group_dict.keys()
        copy_group_dict = deepcopy(group_dict)
        self.remove_excluded_people(copy_group_dict, exclude_list)

        while (len(copy_group_dict.keys()) > 0):
            most_people_group_key = self.get_group_key_with_most_people(copy_group_dict)

            if len(copy_group_dict.keys()) == 1:
                group = copy_group_dict[most_people_group_key]
                while len(group) > 1:
                    person1 = group.pop(random.randint(0, len(group) - 1))
                    person2 = self.random_from_group_dict(copy_group_dict, exclude_people=[person1])
                    pairs.append((person1, person2))
                if len(group) > 0:
                    left_over = group[0]
                    print 'Not enough people. So this week {} does not have a pair'.format(group[0])
                break
            else:
                for i in range(len(copy_group_dict[most_people_group_key])):
                    total_people_minus_group = self.total_people(copy_group_dict, exclude_groups=[most_people_group_key])
                    if total_people_minus_group > 0:
                        group = copy_group_dict[most_people_group_key]
                        person1 = group.pop(random.randint(0, len(group) - 1))
                        person2 = self.random_from_group_dict(copy_group_dict, exclude_groups=[most_people_group_key])
                        pairs.append((person1, person2))
                    else:
                        break
                self.remove_all_empty_groups(copy_group_dict)
        return {'pairs': pairs, 'no_pair': left_over}

    def get_all_people(self, group_dict, exclude_list=[]):
        people = []
        for group_key, group in group_dict.iteritems():
            for person in group:
                if person not in exclude_list:
                    people.append(person)
        return people

    def get_pairs_pure_random(self, group_dict, exclude_list=[]):
        pairs = []
        all_people = self.get_all_people(group_dict, exclude_list)
        while (len(all_people) > 1):
            person_1 = all_people.pop(random.randint(0, len(all_people) - 1))
            person_2 = all_people.pop(random.randint(0, len(all_people) - 1))
            pairs.append((person_1, person_2))
        return {'pairs': pairs, 'no_pair': all_people[0] if len(all_people) > 0 else None}

    def get_pairs(self, group_dict, exclude_list=[]):
        return self.get_pairs_pure_random(group_dict, exclude_list)



