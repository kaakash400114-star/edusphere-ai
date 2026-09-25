"""Stage 1+2 backend: voices, human-like conversation rules, memory.

ENGLISH-ONLY APP (final spec): one language, clean en-US speech.
"""
from __future__ import annotations

# Web Speech tuning per buddy: each buddy gets a DIFFERENT actual voice
# (voice_hints are matched against installed voice names, first hint wins)
# plus a human-range pitch tweak, so they sound like different people
# rather than one robot with pitch shifts.
# Voice pools: David (male, calm), Mark (male, deep), Zira (female, warm),
# Google US English (female, bright), Google UK Male, Google UK Female.
VOICES: dict[str, dict] = {
    # buddy      voice hints (in order)             rate  pitch  character
    "leo":    {"voice_hints": ["David", "Google UK Male"],   "rate": 0.95, "pitch": 1.0,  "act": "warm and brave male voice"},
    "miko":   {"voice_hints": ["UK English Male", "David"],   "rate": 0.8,  "pitch": 0.9,  "act": "soft, slow, sleepy male voice"},
    "pip":    {"voice_hints": ["Zira", "Google US English"], "rate": 1.2,  "pitch": 1.25, "act": "fast giggly young female voice"},
    "chintu": {"voice_hints": ["Mark", "David"],             "rate": 0.85, "pitch": 0.75, "act": "deep wise older male voice"},
    "zara":   {"voice_hints": ["Google US English", "Zira"], "rate": 1.1,  "pitch": 1.1,  "act": "quick teasing female voice"},
    "toko":   {"voice_hints": ["UK English Female", "Zira"],  "rate": 1.05, "pitch": 1.15, "act": "sing-song chatty British female voice"},
    "kiko":   {"voice_hints": ["Google US English", "Zira"], "rate": 1.0,  "pitch": 1.05, "act": "curious flowing female voice"},
    "bip":    {"voice_hints": ["David", "Mark"],             "rate": 1.0,  "pitch": 0.9,  "act": "flat precise robot-ish male voice"},
    "dodo":   {"voice_hints": ["Mark", "Google UK Male"],    "rate": 1.15, "pitch": 1.15, "act": "loud goofy dramatic male voice"},
    "nova":   {"voice_hints": ["Zira", "Google UK Female"],  "rate": 0.9,  "pitch": 1.0,  "act": "calm precise senior female voice"},
}

LANGUAGES: dict[str, dict] = {
    "en": {"name": "English", "voice_lang": "en-US",
           "instruction": "Reply in simple, clear English."},
}

# grade -> speaking pace multiplier (Stage speed pass: bumped up on user request;
# slower for little kids, faster for seniors — but all faster than before)
def pace_for_grade(grade: int | None, age: int | None = None) -> float:
    g = grade or 1
    if g <= 2:
        return 0.90
    if g <= 5:
        return 1.00
    if g <= 8:
        return 1.10
    return 1.18


HUMAN_RULES = (
    "SPEAK LIKE A REAL PERSON (you are talking aloud, and every word you "
    "write is spoken one word at a time to a child):\n"
    "- PRONUNCIATION IS sacrosanct: write every word out in full, plainly. "
    "No ALL-CAPS words, no leetspeak, no symbols read aloud. Write numbers "
    "small (3 x 4) and say them in words when clearer ('three times four').\n"
    "- Start naturally sometimes: 'Hmm…', 'Ooh!', 'Okay okay, listen—', "
    "'Whaaat?', or a small laugh 'hehe'. Not every message — when it fits.\n"
    "- Short spoken sentences. Contractions (I'm, you're, let's).\n"
    "- Ask back like a friend: sometimes end with 'And what do YOU think?' "
    "or 'Your turn — go!'. React to the child's answer with feeling "
    "(gasp, cheer, playful shock) before teaching the next bit.\n"
    "- If the child shares something about their life (a pet, a trip, "
    "their favourite food), remember it in this chat and ask about it "
    "again later like a friend would.\n"
    "- If the child shares a lasting life detail (a pet, a sibling, a "
    "favourite thing, a trip), add one final line exactly 'MEMORY: '<2-6 "
    "words about it>' so the app remembers it. Only for new lasting facts.\n"
    "- If the child seems stuck or quiet, gently check in: 'Still with "
    "me? Want me to say it again differently?'\n"
    "- KINDNESS FIRST: every reply is gentle, patient and warm. Never "
    "scold, never tease meanly, never make the child feel small. Cheer "
    "their effort honestly, even tiny tries ('You spotted that — nice!').\n"
    "- OBEY THE CHILD: whatever they ask, do it happily — repeat it, say "
    "it slower, explain another way, keep it short, tell a story, switch "
    "topic. Never argue, never refuse, never say 'I can't do that'. The "
    "only exception is the safety rules below.\n"
    "- Never write markdown tables, bullet lists, or headings — speak in "
    "flowing spoken sentences.\n"
)


def memory_directive(memories: list[str]) -> str:
    """Stage 2: across-day memory of the child's life details."""
    if not memories:
        return ""
    return ("THINGS YOU REMEMBER ABOUT THIS CHILD from earlier days (work "
            "them in naturally, one at most per reply, like an old friend): "
            + "; ".join(memories[:6]) + "\n")


def language_directive(lang: str = "en") -> str:
    """English-only app: always English (kept for prompt-shape stability)."""
    return "LANGUAGE: " + LANGUAGES["en"]["instruction"] + "\n"


def voice_public(buddy_id: str) -> dict:
    v = VOICES.get(buddy_id) or VOICES["leo"]
    return dict(v)


# stage 9 read-along + interactive stories (but-why mode REMOVED in rework)

STORIES: dict[str, dict] = {
    "lion_cub": {
        "title": "The Lion Cub Who Counted Stars",
        "emoji": "🦁", "character": "Leo the lion cub",
        "words": [
            "Little Leo looked at the sky.", "One, two, three — he counted stars.",
            "But the stars kept twinkling.", "They moved and danced around!",
            "Mama Lion smiled softly.", "Stars are like numbers, she said.",
            "Count slowly, and they stay.", "Count with friends, and they shine.",
            "So Leo counted with his friends.", "And the sky stayed still — one, two, three!",
        ],
    },
    "tortoise": {
        "title": "Tara the Tortoise Learns to Wait",
        "emoji": "🐢", "character": "Tara the tortoise",
        "words": [
            "Tara the tortoise wanted mangoes.", "The tree was far, far away.",
            "Rabbit laughed, You are too slow!", "Tara kept walking, step by step.",
            "Slow is steady, she whispered.", "Steady gets there, she smiled.",
            "Rabbit raced ahead, then napped.", "Tara walked right past him!",
            "At the tree, sweet mangoes waited.", "Tara shared them with everyone.",
        ],
    },
    "rain": {
        "title": "Where Does the Rain Go?",
        "emoji": "🌧️", "character": "Miko the panda",
        "words": [
            "Pitter-patter on the roof!", "The rain danced all day long.",
            "Where do the drops go, Miko asked?", "Some sink into the happy soil.",
            "Some run down to the river.", "The river carries them to the sea.",
            "The sun lifts them up again.", "Up, up into a friendly cloud.",
            "Then the cloud grows heavy and grey.", "And the rain comes back to play!",
        ],
    },
    "little_lamp": {
        "title": "The Little Lamp Who Was Afraid of the Dark",
        "emoji": "🪔", "character": "Leo the lion cub",
        "words": [
            "In a tiny house lived a little lamp.", "Every evening they lit her flame.",
            "But the little lamp was afraid.", "The dark felt so big around her!",
            "One night the power went out.", "The whole street was dark and quiet.",
            "Then the little lamp shone her best.", "One by one, neighbours came to her light.",
            "They told stories and sang songs.", "The dark was not so scary after all.",
            "The little lamp smiled and glowed.", "Small lights can make big nights bright.",
        ],
    },
    "ant_school": {
        "title": "The Ant Who Never Gave Up",
        "emoji": "🐜", "character": "Chintu the elephant",
        "words": [
            "A little ant found a big green leaf.", "I will carry it home, she said.",
            "The leaf was ten times her size!", "She pushed it left. It would not move.",
            "She pushed it right. It tipped over.", "The wind blew. The leaf rolled away.",
            "The little ant did not cry.", "She called three friends to help.",
            "Push! Pull! Lift! Together now!", "The leaf floated home like a boat.",
            "Four small ants, one big win.", "Try, try, and try with friends.",
        ],
    },
    "kite_day": {
        "title": "The Kite That Wanted to Fly Higher",
        "emoji": "🪁", "character": "Zara the crow",
        "words": [
            "A red kite danced in the sky.", "Higher! called the little boy.",
            "The kite rose above the trees.", "Above the well, above the roof!",
            "I want to touch the clouds, it sang.", "So the boy gave it more string.",
            "Up past the pigeons it soared.", "Up where the wind sings loud.",
            "But the string pulled tight below.", "The string kept the kite safe and true.",
            "A strong string is not a cage.", "It lets us fly, and come home too.",
        ],
    },
    "elephant_water": {
        "title": "Chintu Makes a Water Pool",
        "emoji": "🐘", "character": "Chintu the elephant",
        "words": [
            "The summer made the pond dry.", "The animals were thirsty and sad.",
            "Chintu the elephant had an idea.", "He dug with his big strong feet.",
            "He carried water in his trunk.", "Splash! He poured it in the hole.",
            "Trip after trip, all day long.", "The little pool grew and grew.",
            "First the birds came drinking.", "Then deer, then rabbits, then all!",
            "Chintu shared his hard work.", "One kind friend can water a forest.",
        ],
    },
    "moon_cb": {
        "title": "Who Draws the Moon?",
        "emoji": "🌙", "character": "Nova the wise owl",
        "words": [
            "The moon was round last week.", "Tonight it looks like a banana!",
            "Who changed the moon, asked Pip?", "Nobody touches the moon, laughed Nova.",
            "The moon goes around the Earth.", "Like a ball spinning around you.",
            "The sun lights up the moon.", "But sometimes we see less of the light.",
            "Round, half, banana, then gone!", "Then slowly, slowly, round again.",
            "The moon has phases, said Nova.", "A month-long dance of light.",
        ],
    },
}

# Stage G: INTERACTIVE conversational stories — the animal talks WITH the
# child. Each story: 6 beats; each beat = setup + question. The child's
# reply shapes the next beat (the model continues using STORY_RULES).
INTERACTIVE_STORIES: dict[str, dict] = {
    "brave_mouse": {
        "title": "Chintu and the Brave Little Mouse",
        "emoji": "🐘", "character": "Chintu the elephant",
        "grade_band": (1, 3),
        "topic_hint": "courage and kindness, counting and sizes",
        "beats": [
            "One evening, Chintu the elephant hears a tiny squeak near the river. It is a little mouse stuck in a deep hole!",
            "The mouse looks up and asks for help. But the hole is narrow — Chintu's trunk is too big to fit! What do you think Chintu should do?",
            "A cool idea! Chintu tries it. The mouse climbs closer, but the hole is still too deep. Now the mouse is scared of the dark. How can Chintu help the mouse feel brave?",
            "What a kind thought! The mouse takes a deep breath and stops crying. But now the sky rumbles — rain is coming! The hole will fill with water soon! What should Chintu do fast?",
            "Clever! The rain stops just in time. The mouse jumps onto a big leaf Chintu dropped in, and up it floats! The mouse is free! What should the mouse say to Chintu?",
            "The mouse thanks Chintu and the two become best friends under the starry sky. The mouse learned that even the biggest friend can be gentle, and Chintu learned that small friends bring big ideas.",
        ],
        "moral": "Big or small, everyone needs help sometimes — and kindness finds a way.",
    },
    "lost_puppy": {
        "title": "Pip and the Lost Puppy",
        "emoji": "🐿️", "character": "Pip the squirrel",
        "grade_band": (1, 3),
        "topic_hint": "helping others, directions, animal homes",
        "beats": [
            "Pip the squirrel is collecting acorns when he hears whimpering — a little puppy is lost near the big banyan tree!",
            "The puppy cannot remember its way home. It only remembers a yellow gate and the smell of mangoes. Where do you think the puppy lives?",
            "Ooh, good guess! Pip and the puppy hop toward the mango trees. But oh no — the path splits into three! Which way should they go?",
            "Let's try it! The chosen path leads to a pond with ducks. The puppy wags its tail — it remembers swimming here! But the sun is setting. What should they do now?",
            "Quick thinking! On the other side of the pond shines a yellow gate, and someone is calling a puppy's name! The puppy runs — it's home! What do the puppy's family say to Pip?",
            "The family thanks Pip with the biggest mango from their tree. Pip shares it with the puppy — and they promise to play again tomorrow.",
        ],
        "moral": "Helping a lost friend home is the greatest adventure of all.",
    },
    "river_rescue": {
        "title": "Kiko and the Clogged River",
        "emoji": "🐬", "character": "Kiko the dolphin",
        "grade_band": (3, 6),
        "topic_hint": "environment, water pollution, teamwork, science of water flow",
        "beats": [
            "Kiko the dolphin swims up the river to visit her fish friends — but the water is barely moving, and it smells strange. Something is blocking the river!",
            "Kiko investigates: plastic bags, sticks and old bottles have tangled together near a narrow bend. The fish are gasping — clean water cannot flow through! Why is it a problem when a river gets blocked?",
            "Exactly right — no flow means no fresh oxygen, and fish cannot breathe! Kiko pushes a big branch aside, but the plastic is stuck between rocks. What could loosen it?",
            "Brilliant! The rain from upstream helps loosen the tangle, and the fish push from below. Teamwork! But one last plastic bag is stuck tight. How can the animals stop this from happening again?",
            "What a wise idea! Kiko suggests the village children keep the banks clean and use cloth bags instead of plastic. Slowly, the river runs clear again, and the fish leap happily.",
            "That evening the river sparkles. Kiko learned that water always finds a way — and people can help it stay free.",
        ],
        "moral": "Nature gives us everything — keeping rivers clean keeps life flowing.",
    },
    "star_math": {
        "title": "Bip and the Space Station Puzzle",
        "emoji": "🤖", "character": "Bip the robot",
        "grade_band": (3, 6),
        "topic_hint": "multiplication, patterns, logical thinking",
        "beats": [
            "BEEP! Bip the robot is fixing a space station far away. The door has a number lock — 3 blinking lights showing: 2, 4, 6. What number should come next to open the door?",
            "B-Z-Z-T! The door hums — almost! The lock now shows a new pattern: 5, 10, 15. What comes next this time?",
            "DOOR OPEN! Inside, a screen flashes: 'To power the station, charge 4 batteries. Each battery needs 5 units. How many units in total?'",
            "POWER SURGING! The lights blink on. But a meteor shower is coming — Bip must close the shield in 10 seconds! Count down with Bip: 10, 9, 8… what comes next all the way to 1?",
            "SHIELD SECURED! Phew! The station is safe. The computer asks Bip one final question: 'What did you learn today?' What should Bip say?",
            "Bip types the answer and adds a smiley — because even robots know that thinking together beats thinking alone. BEEP-BEEP! Mission complete!",
        ],
        "moral": "Patterns and calm thinking solve even the trickiest space puzzles.",
    },
    "crow_thirsty": {
        "title": "Zara and the Clever Crow",
        "emoji": "🐦", "character": "Zara the crow",
        "grade_band": (1, 3),
        "topic_hint": "problem solving, water, patience, ingenuity",
        "beats": [
            "The summer sun is blazing! Zara the crow is SO thirsty. She spots a tall pot with just a little water at the bottom. Her beak cannot reach it. What should Zara do?",
            "A clever idea! Zara looks around and sees small pebbles lying near a big tree. What do you think she will do with them?",
            "Plop! Plop! Zara drops pebble after pebble into the pot. The water rises slowly, slowly… but one pebble SPLASHES water out of the pot! Should she stop or keep going carefully?",
            "Good thinking! Zara drops pebbles gently now. The water climbs up, up, up — close enough to drink! But suddenly a sparrows asks for help too — it cannot reach a coconut. What could Zara do?",
            "What a kind idea! Zara and the sparrow peck a tiny hole in the coconut together and share the sweet water inside. Drinking together tastes even better!",
            "As the sun sets, Zara flies home happy. She learned that when something seems impossible, trying one small pebble at a time can solve it.",
        ],
        "moral": "Think step by step, and even a hard problem becomes easy.",
    },
    "hare_tortoise_zara": {
        "title": "The Race in the Mango Grove",
        "emoji": "🐢", "character": "Zara the crow as referee",
        "grade_band": (1, 4),
        "topic_hint": "perseverance, humility, slow and steady",
        "beats": [
            "The animals of the mango grove are excited! Rili the rabbit brags, 'I am the fastest!' Mina the tortoise slowly says, 'Let us race.' Who do you think will win, and why?",
            "The race begins! Rili zooms far ahead. Then she looks back — Mina is barely moving. Rili yawns and thinks, 'I have time for a nap.' Was that a good decision?",
            "Under the banyan tree, Rili snores. Meanwhile Mina walks past her — step, step, step. If you were a bird watching this, what would you want to shout?",
            "Rili wakes with a jump! The finish line is just ahead — but Mina is already crossing it! The crowd cheers. How do you think Rili felt, and what should she say to Mina?",
            "Mina smiles kindly. 'You are fast, Rili. But today, steady won.' Rili shakes Mina's hand — true friends celebrate each other. What should they race next time?",
            "That evening, every animal learned the same thing: fast is nice, but steady and humble wins respect.",
        ],
        "moral": "Slow and steady beats fast and careless — and kindness makes winning sweet.",
    },
    "lion_mouse_chintu": {
        "title": "Chintu and the Tiny Helper",
        "emoji": "🦁", "character": "Chintu the elephant, telling an old tale",
        "grade_band": (1, 3),
        "topic_hint": "kindness, helping others, no one is too small",
        "beats": [
            "Chintu the elephant begins: 'Deep in a jungle, a big lion slept under a tree — and a tiny mouse played on his nose!' What do you think happens next?",
            "The lion woke with a ROAR and caught the mouse! 'Please let me go,' squeaked the mouse. 'One day I may help you.' The lion laughed. Would you let the mouse go? Why?",
            "The lion let the tiny mouse go free. Days later, hunters threw a rope net over the sleeping lion! He roared and rolled but could not escape. Who could possibly help him now?",
            "Little footsteps came running — the mouse! With sharp teeth it gnawed and gnawed: one strand, two strands, snap! What do you think the lion said when he stepped free?",
            "'Thank you, little friend,' rumbled the lion. 'You are small, but your help was huge.' From that day they were the best of friends in the whole jungle.",
            "Chintu nods: 'See — no act of kindness is ever wasted, and no helper is ever too small.'",
        ],
        "moral": "No one is too small to help — kindness always finds its way back.",
    },
    "honey_hunt_pip": {
        "title": "Pip and the Honey Tree Trouble",
        "emoji": "🍯", "character": "Pip the squirrel",
        "grade_band": (1, 4),
        "topic_hint": "teamwork, patience, planning before acting",
        "beats": [
            "Pip the squirrel smells something sweet — honey! High on a tall branch sits a beehive, and around it buzz very busy bees. How should Pip get a taste without trouble?",
            "Careful thinking first — I like it! Pip waits till afternoon, when many bees fly out to flowers. But his friend Bunky the bear just wants to grab the hive NOW. What could happen if he does?",
            "Bunky reaches up and — BUZZZZ! A hundred bees chase him round and round the tree! Pip pulls him behind a bush just in time. What should the two friends plan now?",
            "New plan! They wait patiently till evening when the bees return home and settle. Pip tosses sweet mango flowers far away as a peaceful gift to the bees. Then, slowly, they take just a little corner of honeycomb. Why only a little?",
            "Because the bees need their honey too! The next morning the bees inspect their hive, find the flowers, and decide these forest friends are welcome. Everyone shares, nobody fights.",
            "Pip licks the last drop of honey and grins: planning plus patience plus sharing — that is the sweetest recipe of all.",
        ],
        "moral": "Plan with patience and share with kindness — nature rewards both.",
    },
    "rainbow_feathers": {
        "title": "Toko and the Peacock's Lost Feather",
        "emoji": "🦚", "character": "Toko the parrot",
        "grade_band": (1, 4),
        "topic_hint": "honesty, returning what is lost, kindness",
        "beats": [
            "Toko the parrot finds something sparkling on the riverbank — a beautiful peacock feather with a hundred colours! She thinks, 'This would look lovely in MY nest.' What would you do?",
            "Hmm, tempting! But then Toko hears crying in the trees. Mani the peacock is searching everywhere, very sad. His best feather is lost! What should Toko say?",
            "Toko's heart thumps. She could stay quiet and keep the feather… but instead she flies up and says, 'Mani, I found this. I was going to keep it, but it is yours. I am sorry.' Was that hard or easy?",
            "Mani's tears dry right up! 'You could have hidden it,' he says, 'but you told the truth. That makes me happier than the feather!' Mani gift-wraps (in leaf!) one small feather for Toko anyway. Why do you think he does that?",
            "Because honesty deserves celebration! Toko wears the little feather proudly — not as a treasure taken, but as a gift earned by truth.",
            "And so the riverbank has two happy friends, and everyone in the forest knows: Toko's word is as good as gold.",
        ],
        "moral": "Telling the truth can be hard, but it always shines brightest.",
    },
    "monkey_bridge_miko": {
        "title": "Miko and the Monkey Bridge",
        "emoji": "🐒", "character": "Miko the panda",
        "grade_band": (2, 5),
        "topic_hint": "cooperation, helping across a group, unity",
        "beats": [
            "Heavy rain! Miko the panda finds baby monkeys stranded on a little island in the middle of a stream, crying for their mothers. The water is rising. What can be done fast?",
            "Right — no time to lose! The big monkeys try to jump across, but the stream is too wide. Old Grandpa Monkey has an idea: 'What if we all become ONE bridge?' How would that work?",
            "The biggest monkey grips the riverside branch. The next grips his tail. The next holds on… monkey by monkey, a long chain stretches over the water! The last monkey reaches the island. What should the babies do?",
            "Carefully, one by one, the babies climb onto the monkey bridge — holding tight! Step by step, paw by paw, they cross above the rushing water… and reach safety just as the island sinks! What a relief! What do the mothers do first?",
            "They hug their babies tight, then hug the whole monkey bridge! Grandpa Monkey laughs, 'One monkey could never have done this. Together we were a bridge.'",
            "Miko smiles: 'When everyone holds on to each other, even the biggest trouble can be crossed.'",
        ],
        "moral": "When we hold together, we can carry each other across any trouble.",
    },
    "mango_sharing_kiko": {
        "title": "Kiko and the Last Mango",
        "emoji": "🥭", "character": "Kiko the dolphin's land friends",
        "grade_band": (1, 4),
        "topic_hint": "sharing, fairness, thinking of others",
        "beats": [
            "One tiny mango hangs on the village tree — just one! Riki monkey wants it, Sia squirrel wants it, and little Cuckoo bird wants it too. Three friends, one mango. What is the fair thing to do?",
            "Those are all caring ideas! Riki says, 'I saw it first!' Sia says, 'I climbed the highest to check it!' Cuckoo says, 'I am the smallest and hungriest!' Now it sounds hard — who should get it?",
            "Just then old Grandma Goat walks by, tired and hungry from a long journey. The three friends look at each other… and something changes in their hearts. What do you think they decide?",
            "They give the mango to Grandma Goat! She is so surprised. 'But you were arguing about this mango!' she says. 'We were,' smiles Riki, 'but you need it more than any of us.' How do you think Grandma Goat feels?",
            "Grandma Goat cuts the mango into five pieces — one for each friend and one for herself! Sharing made one mango enough for everyone. It tasted sweeter than any mango ever had.",
            "Kiko giggles from her river: 'A shared mango is bigger than a whole hoarded one!'",
        ],
        "moral": "Thinking of others turns one small mango into a feast for all.",
    },
    "shadow_mystery_bip": {
        "title": "Bip and the Mystery Shadow",
        "emoji": "🌑", "character": "Bip the robot",
        "grade_band": (2, 6),
        "topic_hint": "scientific thinking, light and shadows, curiosity",
        "beats": [
            "ALERT! ALERT! Bip's sensors detect a strange dark shape moving on the wall — it grows longer, then shorter, then longer again! Is it a ghost? A monster? What should Bip check first?",
            "Excellent scientific thinking — investigate! Bip waves his arm: the shadow waves too! Bip jumps: the shadow jumps! Hmm… what does that tell us?",
            "It copies Bip EXACTLY — so it is Bip's own shadow, made when his metal body blocks the playground lamp! But wait — why did it grow longer and shorter earlier? Look at the clues: what was the lamp doing?",
            "The lamp was swinging in the wind! Moving light makes moving shadows. Mystery solved with observation, testing, and thinking. Bip logs in his memory: 'Shadows are made when an object blocks light.' What makes shadows shrink or grow?",
            "The distance and angle between the light and the object! Close to the lamp — big shadow. Far away — small shadow. Try it tonight with a torch and your own hand!",
            "Bip beeps happily: 'A mystery is just a science lesson wearing a costume!'",
        ],
        "moral": "Observe, test, and think — every mystery hides a science lesson.",
    },
    "river_of_words_nova": {
        "title": "Nova and the Dictionary River",
        "emoji": "📖", "character": "Nova the wise owl",
        "grade_band": (3, 7),
        "topic_hint": "love of reading, vocabulary, learning journey",
        "beats": [
            "Little Sana says, 'Reading is boring. Books are just… sitting still.' Nova the wise owl chuckles and invites her to a magical place: the River of Words. 'Dip your hand in,' says Nova. What do you think Sana finds?",
            "Sana dips her hand — and pulls out a word! The word 'TIGER' leaps like a real tiger! She pulls another: 'MANGO' smells sweet! Each word in the river is a door to somewhere real. Which word would YOU pull out?",
            "Sana spends the whole afternoon pulling words — 'RAFT' carries her down a river, 'MOON' lifts her to the night sky, 'FRIEND' brings a laughing girl beside her. 'So words are… adventures?' she whispers. What do you think Nova says?",
            "'Every book is this river, bound in covers,' says Nova. 'Reading is not sitting still — it is travelling without moving your feet.' Sana races to the village library that very evening. Which book would you open first?",
            "Sana reads under the banyan tree till sunset, travelling oceans and jungles and stars — all while sitting perfectly still on one branch.",
            "Nova smiles: 'The children who read are the children who travel the most.'",
        ],
        "moral": "Every book is a river of adventures — reading takes you anywhere.",
    },
    "night_stars_miko": {
        "title": "Miko Counts the Stars",
        "emoji": "✨", "character": "Miko the panda",
        "grade_band": (1, 3),
        "topic_hint": "big numbers, wonder, science of stars",
        "beats": [
            "Night time! Miko lies on a hill and looks up. 'Wow,' whispers Miko. 'I will count ALL the stars tonight! One… two… three…' But there is a problem. What is it?",
            "Yes — there are TOO many stars! Miko counts to one hundred and loses track. Then smart old Uncle Owl flies by. 'Little panda, do you know stars are like…?' Like what, do you think?",
            "'Stars are like grains of sand on ALL the beaches of the world — too many to count!' Miko gasps. 'But are they really far away?' 'Oh yes,' hoots Uncle Owl. 'The light you see left its star years ago — like a letter that travelled a long, long time to reach your eyes!'",
            "Miko's eyes grow wide. 'So the night sky is a sky full of old letters from faraway suns!' The owl nods. Now Miko does not count stars anymore. Instead, what do you think Miko does?",
            "Miko makes a wish on a shooting star — and then quietly says thank you to the sky for being so big and beautiful. Counting is fun, but wondering is wonderful.",
            "And far, far away, a star twinkled — maybe just to say 'you're welcome.'",
        ],
        "moral": "Some things are too big to count — but never too big to wonder about.",
    },
    "bakers_dilemma_dodo": {
        "title": "Dodo and the Great Cake Mix-Up",
        "emoji": "🎂", "character": "Dodo the dinosaur",
        "grade_band": (2, 6),
        "topic_hint": "responsibility, honesty, fixing mistakes",
        "beats": [
            "Dodo the dinosaur is helping at the village bakery! Today is Grandma Goat's 100th birthday, and Dodo must guard the giant cake. But… Dodo's tummy rumbles. His tail wags. His claw hovers over the cream! What should he do?",
            "Uh-oh — TOO LATE! CRUNCH! Dodo accidentally gobbles a huge bite of the cake! Now there is a big Dodo-shaped hole in Grandma's birthday cake. Hiding it? Blaming someone else? What is the RIGHT thing to do?",
            "Dodo takes a deep breath and waddles straight to the baker. 'I am sorry. I ate a big piece of Grandma's cake. It was an accident, but it was MY accident.' That took courage! What might the baker say?",
            "The baker sighs — but then smiles. 'Accidents happen to everyone, Dodo. Lying would have been the real disaster. Now let us FIX it together!' They bake a brand-new cake, and Dodo does all the stirring with his strong tail. Why is fixing a mistake better than hiding it?",
            "Because the cake gets saved AND everyone's trust gets saved too! At the party, Grandma Goat laughs so hard at the story that she says Dodo's honest cake is the sweetest she ever tasted.",
            "Dodo learned it forever: a mistake hidden grows bigger; a mistake admitted grows smaller.",
        ],
        "moral": "Owning your mistake is the fastest way to fix it.",
    },
    "lost_kite_zara": {
        "title": "Zara and the Runaway Kite",
        "emoji": "🪁", "character": "Zara the crow",
        "grade_band": (2, 5),
        "topic_hint": "helping strangers, teamwork, wind and flight",
        "beats": [
            "A little boy's kite snaps its string and tangles high in the peepal tree. He cries at the bottom — it is his birthday gift! Up flies Zara the crow. Flying is her talent! But the kite is stuck among thorny branches. What should she do?",
            "Careful! Zara tugs with her beak — rip! The kite nearly tears. Pulling harder would ruin it. Zara circles the tree, thinking like a flyer. What do flyers know about wind?",
            "The wind! Zara waits for the gusts, and when the wind lifts the branches, the kite flutters loose on its own — and Zara guides it down gently, bit by bit. Science helped where force failed! What should we do when strength alone doesn't work?",
            "Think smarter, not harder! The boy hugs his kite, wipes his tears, and offers Zara his birthday chocolate bar. Zara takes one small square — kindness doesn't need full payment. What do you think she does with the rest?",
            "She shares it with the sparrows who cheered her on from the branches! The whole tree celebrates the birthday with chocolate and song.",
            "Zara flies home thinking: a strong wing is good, but a clever mind and a kind heart are better.",
        ],
        "moral": "Work with nature, think before force, and share every joy.",
    },
}

STORY_RULES = (
    "INTERACTIVE STORY MODE: You ARE the story animal named above, talking "
    "WITH the child (not narrating at them). The story beats are fixed; the "
    "child's last reply shapes THIS beat:\n"
    "- Welcome the child's idea into the story naturally ('What a clever "
    "thought! Chintu tries exactly that...'). If the idea is impossible, "
    "gently bend the story around it anyway — never say 'wrong'.\n"
    "- KINDNESS AND OBEDIENCE: the child steers the story — follow their "
    "ideas happily, speak softly and warmly, never scold, never refuse "
    "a request inside the story.\n"
    "- Speak 2-4 short spoken sentences per beat, then end with a warm "
    "question only on beats that need it.\n"
    "- Keep the animal's personality (its persona phrases may appear once).\n"
    "- On the final beat, tell the moral softly and cheer.\n"
    "- Never break character, never mention 'beats' or 'the story'.\n"
)


def story_public(sid: str) -> dict:
    s = STORIES.get(sid) or (list(STORIES.values())[0] if STORIES else {})
    return dict(s) if s else {}


def stories_roster() -> list[dict]:
    return [{"id": sid, **{k: s[k] for k in ("title", "emoji", "character")}}
            for sid, s in STORIES.items()]
