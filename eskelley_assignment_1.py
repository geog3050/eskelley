def hawkid():
    return(["Emma Skelley", "eskelley"])
def import_data(filename):
    participants = []
    with open(filename, 'r') as source:
        for line in source:
            fields = line.strip().split(',')
            health = float(fields[2])
            damage = float(fields[3])
            row = [fields[0], fields[1], health, damage]
            participants.append(row)
    return participants
def attack_multiplier(attacker_type, defender_type):
    if attacker_type == 'Water' and defender_type == 'Fire':
        return 2.5
    elif attacker_type == 'Electric' and defender_type =='Water':
        return 1.3
    elif attacker_type == 'Ground' and defender_type == 'Electric': 
        return 2.0
    elif attacker_type == 'Fire' and defender_type =='Grass':
        return 3.0
    elif attacker_type == 'Grass' and defender_type == 'Water':
        return 1.5
    else:
        return 1.0
def fight(participant1, participant2, first2attack):
    rounds  = 0
    health1 = participant1[2]
    health2 = participant2[2]
    type1 = participant1[1]
    type2 = participant2[1]
    while health1 > 0 and health2 > 0:
        if first2attack == 1:
            multiplier = attack_multiplier(type1, type2)
            health2 -= participant1[3] * multiplier
        elif first2attack == 2:
            multiplier = attack_multiplier(type2, type1)
            health1 -= participant2[3] * multiplier
        rounds += 1
        if first2attack == 1:
            first2attack = 2
        else:
            first2attack = 1
    if health1 > 0:
        winner = 1
    elif health2 > 0:
        winner = 2
    return [winner, rounds]
def tournament(participants):
    wins = [0, 0, 0, 0, 0, 0]
    for i in range(len(participants)):
        for j in range (i + 1, len(participants)):
            p1 = participants[i]
            p2 = participants[j]
            home = fight(p1, p2, 1)
            away = fight(p1, p2, 2)
            #print(p1, p2, home, away)
            if home[0] == 1:
                wins[i] +=1
            elif home[0] == 2:
                wins[j] +=1
            if away[0] == 1:
                wins[i] += 1
            elif away[0] ==2:
                wins[j] +=1
    return wins
