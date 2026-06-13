#!/usr/bin/env python3
import os
import re

VAULT_DIR = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
MATIKA_DIR = os.path.join(VAULT_DIR, "matika")

# Database of unique factors
FACTORS = {
    # 1. Four Noble Truths
    "suffering": {
        "title_en": "Suffering / Unsatisfactoriness",
        "title_pali": "Dukkha",
        "def_pali": "Cattāri ariyasaccāni: dukkhaṃ ariyasaccaṃ...",
        "def_en": "The Four Noble Truths: the noble truth of suffering...",
        "description": "Dukkha is the fundamental unsatisfactoriness of conditioned existence. It encompasses physical pain (dukkha-dukkha), the suffering of change and impermanence (vipariṇāma-dukkha), and the pervasive unsatisfactoriness of conditioned formations (saṅkhāra-dukkha). Understanding dukkha is the first step toward liberation.",
        "parents": ["four_noble_truths", "three_marks"],
        "suttas": ["[SN 56.11: Dhammacakkappavattanasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "origin_of_suffering": {
        "title_en": "Origin of Suffering",
        "title_pali": "Samudaya",
        "def_pali": "Yāyaṃ taṇhā ponobhavikā nandirāgasahagatā...",
        "def_en": "It is this craving which leads to new rebirth, accompanied by delight and lust...",
        "description": "Samudaya refers to the cause of suffering, identified as craving (taṇhā) of three kinds: craving for sensual pleasures (kāma-taṇhā), craving for existence/becoming (bhava-taṇhā), and craving for non-existence (vibhava-taṇhā). This craving keeps beings bound to the wheel of rebirth.",
        "parents": ["four_noble_truths"],
        "suttas": ["[SN 56.11: Dhammacakkappavattanasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "cessation_of_suffering": {
        "title_en": "Cessation of Suffering",
        "title_pali": "Nirodha",
        "def_pali": "Yo tassāyeva taṇhāya asesavirāganirodho cāgo paṭinissaggo...",
        "def_en": "The remainderless fading away and cessation of that same craving, its discarding and relinquishing...",
        "description": "Nirodha is the cessation of suffering, synonymous with Nibbāna. It is achieved by the complete fading away, relinquishing, and ending of craving. When craving is extinguished, the cycle of birth and death ceases, and absolute peace is realized.",
        "parents": ["four_noble_truths"],
        "suttas": ["[SN 56.11: Dhammacakkappavattanasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "path_to_cessation": {
        "title_en": "Path to Cessation",
        "title_pali": "Magga",
        "def_pali": "Ayameva ariyo aṭṭhaṅgiko maggo, seyyathidaṃ—sammādiṭṭhi...",
        "def_en": "It is this Noble Eightfold Path, that is: right view...",
        "description": "Magga is the way of practice leading to the cessation of suffering. It is the Noble Eightfold Path (*Ariyo Aṭṭhaṅgiko Maggo*), which is divided into the three trainings: wisdom (*paññā*), ethical conduct (*sīla*), and mental concentration (*samādhi*). It is the middle way between indulgence and self-mortification.",
        "parents": ["four_noble_truths"],
        "suttas": ["[SN 56.11: Dhammacakkappavattanasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },

    # 2. Three Marks of Existence
    "impermanence": {
        "title_en": "Impermanence / Inconstancy",
        "title_pali": "Anicca",
        "def_pali": "Yadaniccaṃ taṃ dukkhaṃ...",
        "def_en": "What is impermanent is suffering...",
        "description": "Anicca is the mark of impermanence. All conditioned phenomena, physical or mental, are in a state of constant flux, arising and passing away from moment to moment. Clinging to what is impermanent inevitably leads to suffering (*dukkha*).",
        "parents": ["three_marks"],
        "suttas": ["[SN 22.59: Anattalakkhaṇasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[Dhp Ch. 20: Maggavagga](../mula/sutta/khuddaka_nikaya/dhammapada/dhp_20_maggavagga.md)"]
    },
    "non_self": {
        "title_en": "Non-self / Egolessness",
        "title_pali": "Anattā",
        "def_pali": "Rūpaṃ, bhikkhave, anattā...",
        "def_en": "Form, bhikkhus, is non-self...",
        "description": "Anattā is the mark of non-self. No conditioned or unconditioned phenomenon contains a permanent, independent, or unchanging self, soul, or essence. Experience is comprised of empty processes rising and passing according to causes.",
        "parents": ["three_marks"],
        "suttas": ["[SN 22.59: Anattalakkhaṇasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[Dhp Ch. 20: Maggavagga](../mula/sutta/khuddaka_nikaya/dhammapada/dhp_20_maggavagga.md)"]
    },

    # 3. Five Aggregates & Dependent Origination
    "form_or_matter": {
        "title_en": "Form / Matter",
        "title_pali": "Rūpa",
        "def_pali": "Cattāro ca mahābhūtā, catunnañca mahābhūtānaṃ upādāyarūpaṃ...",
        "def_en": "The four great elements and form derived from them...",
        "description": "Rūpa refers to the physical aspect of existence, comprising the four great elements (earth/solidity, water/cohesion, fire/temperature, wind/motion) and physical matter derived from them. It represents the material base of sentient experience.",
        "parents": ["five_aggregates"],
        "suttas": ["[SN 22.59: Anattalakkhaṇasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "feeling": {
        "title_en": "Feeling / Sensation",
        "title_pali": "Vedanā",
        "def_pali": "Tisso vedanā—sukhā vedanā, dukkhā vedanā, adukkhamasukhā vedanā...",
        "def_en": "Three feelings: pleasant feeling, painful feeling, neutral feeling...",
        "description": "Vedanā is the affective tone of experience. Every sensory contact is experienced as pleasant, unpleasant, or neutral. Feeling is not emotion, but the raw sensation that, if met with ignorance, triggers craving and aversion.",
        "parents": ["five_aggregates", "dependent_origination", "four_foundations_of_mindfulness"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[MN 43: Mahāvedallasutta](../mula/sutta/majjhima_nikaya/mn43.md)"]
    },
    "perception": {
        "title_en": "Perception / Recognition",
        "title_pali": "Saññā",
        "def_pali": "Saññākkhandho: rūpasaññā, saddasaññā, gandhasaññā...",
        "def_en": "The perception of forms, sounds, smells...",
        "description": "Saññā is the mental faculty that recognizes, names, and labels sensory data. It compares current experience with past memories to identify objects (e.g. recognizing a color or shape). It is prone to distortion and illusion.",
        "parents": ["five_aggregates"],
        "suttas": ["[DN 9: Poṭṭhapādasutta](../mula/sutta/digha_nikaya/dn9.md)", "[SN 22.95: Phenapiṇḍūpamasutta](../mula/sutta/samyutta_nikaya/INDEX.md)"]
    },
    "volitional_formations": {
        "title_en": "Volitional Formations",
        "title_pali": "Saṅkhārā",
        "def_pali": "Saṅkhārakkhandho: rūpasañcetanā, saddasañcetanā...",
        "def_en": "Volition regarding forms, sounds...",
        "description": "Saṅkhārā refers to the active, fabricating forces of the mind. It encompasses intentions, choices, habits, and emotional responses that shape kamma. It is the constructive activity of consciousness.",
        "parents": ["five_aggregates", "dependent_origination"],
        "suttas": ["[SN 22.59: Anattalakkhaṇasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[SN 22.95: Phenapiṇḍūpamasutta](../mula/sutta/samyutta_nikaya/INDEX.md)"]
    },
    "consciousness": {
        "title_en": "Consciousness / Awareness",
        "title_pali": "Viññāṇa",
        "def_pali": "Chacete viññāṇakāyā: cakkhuviññāṇaṃ, sotaviññāṇaṃ...",
        "def_en": "Six classes of consciousness: eye-consciousness, ear-consciousness...",
        "description": "Viññāṇa is the basic cognizing awareness that arises when a sense organ meets a sense object. It is divided into six classes based on the sense doors (eye, ear, nose, tongue, body, intellect). It provides the field for experience.",
        "parents": ["five_aggregates", "dependent_origination"],
        "suttas": ["[MN 43: Mahāvedallasutta](../mula/sutta/majjhima_nikaya/mn43.md)", "[MN 44: Cūḷavedallasutta](../mula/sutta/majjhima_nikaya/mn44.md)"]
    },
    "ignorance": {
        "title_en": "Ignorance",
        "title_pali": "Avijjā",
        "def_pali": "Dukkhe aññāṇaṃ, samudaye aññāṇaṃ...",
        "def_en": "Non-knowledge of suffering, non-knowledge of its origin...",
        "description": "Avijjā is the root cause of saṃsāra and suffering. It is not a mere lack of facts, but the active delusion that misperceives the impermanent as permanent, the unsatisfactory as satisfying, and the non-self as self. It is defined as ignorance of the Four Noble Truths.",
        "parents": ["dependent_origination", "ten_fetters"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[MN 9: Sammādiṭṭhisutta](../mula/sutta/majjhima_nikaya/mn9.md)"]
    },
    "name_and_form": {
        "title_en": "Name and Form",
        "title_pali": "Nāmarūpa",
        "def_pali": "Vedanā, saññā, cetanā, phasso, manasikāro—idaṃ vuccati nāmaṃ; cattāro ca mahābhūtā...",
        "def_en": "Feeling, perception, intention, contact, attention—this is called name; the four great elements...",
        "description": "Nāmarūpa is the junction of mental factors ('name' — feeling, perception, intention, contact, attention) and material factors ('form' — elements and matter). It represents the psycho-physical organism required for experience to take place.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[MN 9: Sammādiṭṭhisutta](../mula/sutta/majjhima_nikaya/mn9.md)"]
    },
    "six_sense_fields": {
        "title_en": "Six Sense Fields",
        "title_pali": "Saḷāyatana",
        "def_pali": "Cakkhāyatanaṃ, sotāyatanaṃ, ghānāyatanaṃ...",
        "def_en": "The eye base, the ear base, the nose base...",
        "description": "Saḷāyatana refers to the six internal organs of perception (eye, ear, nose, tongue, body, mind) and their corresponding six external spheres of objects (forms, sounds, smells, tastes, touches, ideas). They are the gateways of contact.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[MN 148: Chachakkasutta](../mula/sutta/majjhima_nikaya/mn148.md)"]
    },
    "contact": {
        "title_en": "Contact / Sensory Impingement",
        "title_pali": "Phassa",
        "def_pali": "Chayime phassakāyā: cakkhusamphasso, sotasamphasso...",
        "def_en": "Six classes of contact: eye-contact, ear-contact...",
        "description": "Phassa is the coming together of three things: a sense organ, a sense object, and the corresponding consciousness. Contact is the spark that ignites experience, serving as the necessary condition for feeling (*vedanā*) to arise.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[MN 148: Chachakkasutta](../mula/sutta/majjhima_nikaya/mn148.md)"]
    },
    "craving": {
        "title_en": "Craving",
        "title_pali": "Taṇhā",
        "def_pali": "Chayime taṇhākāyā: rūpataṇhā, saddataṇhā...",
        "def_en": "Six classes of craving: craving for forms, craving for sounds...",
        "description": "Taṇhā is the thirst, desire, or feverish demand for experience. It arises conditioned by feeling (*vedanā*) and manifests in three ways: craving for sensuality (kāma-taṇhā), for existence (bhava-taṇhā), and for non-existence (vibhava-taṇhā). It drives all suffering and rebirth.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[SN 56.11: Dhammacakkappavattanasutta](../mula/sutta/samyutta_nikaya/INDEX.md)"]
    },
    "clinging_or_grasping": {
        "title_en": "Clinging / Grasping",
        "title_pali": "Upādāna",
        "def_pali": "Cattāri upādānāni: kāmupādānaṃ, diṭṭhupādānaṃ, sīlabbatupādānaṃ, attavādupādānaṃ...",
        "def_en": "Four kinds of clinging: clinging to sensuality, clinging to views, clinging to rules and vows, clinging to self-theory...",
        "description": "Upādāna is the intensification of craving. It is the active holding on, grasping, or identification with four domains: sensuality, speculative views, external rules/vows, and theories of a permanent self. It solidifies the sense of 'I' and 'mine'.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[MN 44: Cūḷavedallasutta](../mula/sutta/majjhima_nikaya/mn44.md)"]
    },
    "existence_or_becoming": {
        "title_en": "Existence / Becoming",
        "title_pali": "Bhava",
        "def_pali": "Tayo me bhavā: kāmabhavañca, rūpabhavañca, arūpabhavañca...",
        "def_en": "Three kinds of existence: sensual existence, material existence, immaterial existence...",
        "description": "Bhava is the process of becoming. It is the active kamma-process (*kammabhava*) that creates the conditions for future rebirth (*uppattibhava*) across the three realms of existence: the sensual realm, the fine-material realm, and the immaterial realm.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[MN 9: Sammādiṭṭhisutta](../mula/sutta/majjhima_nikaya/mn9.md)"]
    },
    "birth": {
        "title_en": "Birth",
        "title_pali": "Jāti",
        "def_pali": "Yā tesaṃ tesaṃ sattānaṃ tamhi tamhi sattanikāye jāti sañjāti...",
        "def_en": "The birth, conception, production, manifestation of aggregates of various beings...",
        "description": "Jāti is the entry of consciousness into a new physical existence. It is defined as the birth, conception, and manifestation of the aggregates and acquisition of the sense bases in any realm, representing the start of a new cycle of suffering.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[DN 15: Mahānidānasutta](../mula/sutta/digha_nikaya/dn15.md)"]
    },
    "aging_and_death": {
        "title_en": "Aging and Death",
        "title_pali": "Jarāmaraṇa",
        "def_pali": "Yā tesaṃ tesaṃ sattānaṃ jarā jīrānataṃ... yaṃ tesaṃ tesaṃ sattānaṃ maraṇaṃ...",
        "def_en": "The decay, decrepitude, brokenness... the passing away, dissolution, disappearance of various beings...",
        "description": "Jarāmaraṇa is the inevitable decay, decrepitude, and final dissolution of the psycho-physical organism. It represents the culmination of birth, followed by grief, lamentation, pain, distress, and despair.",
        "parents": ["dependent_origination"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[DN 15: Mahānidānasutta](../mula/sutta/digha_nikaya/dn15.md)"]
    },

    # 4. Ethics / Precepts
    "abstaining_from_killing": {
        "title_en": "Abstaining from Killing",
        "title_pali": "Pāṇātipātā veramaṇī",
        "def_pali": "Pāṇātipātā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from taking life...",
        "description": "The first precept of Buddhist ethics. It requires refraining from deliberately destroying, harming, or shortening the life of any living creature. It is motivated by loving-kindness and compassion for all life.",
        "parents": ["five_precepts", "eight_precepts"],
        "suttas": ["[AN 11.15: Karaṇīyamettāsutta](../mula/sutta/anguttara_nikaya/an11_15.md)", "[matika/five_precepts](five_precepts.md)"]
    },
    "abstaining_from_stealing": {
        "title_en": "Abstaining from Stealing",
        "title_pali": "Adinnādānā veramaṇī",
        "def_pali": "Adinnādānā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from taking what is not given...",
        "description": "The second precept. It requires refraining from theft, fraud, or taking others' property without permission. It encourages honesty, respect for others, and active generosity.",
        "parents": ["five_precepts", "eight_precepts"],
        "suttas": ["[matika/five_precepts](five_precepts.md)", "[matika/eight_precepts](eight_precepts.md)"]
    },
    "abstaining_from_sexual_misconduct": {
        "title_en": "Abstaining from Sexual Misconduct",
        "title_pali": "Kāmesumicchācārā veramaṇī",
        "def_pali": "Kāmesumicchācārā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from sexual misconduct...",
        "description": "The third precept for lay practitioners. It requires refraining from adultery, exploitation, abuse, or any sexual action that violates trust and commitments. It preserves relational harmony and respect.",
        "parents": ["five_precepts"],
        "suttas": ["[matika/five_precepts](five_precepts.md)"]
    },
    "abstaining_from_false_speech": {
        "title_en": "Abstaining from False Speech",
        "title_pali": "Musāvādā veramaṇī",
        "def_pali": "Musāvādā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from false speech...",
        "description": "The fourth precept. It requires refraining from deliberate lying, deceit, and misrepresentation. It protects truthfulness, trust, and integrity in communication.",
        "parents": ["five_precepts", "eight_precepts"],
        "suttas": ["[matika/five_precepts](five_precepts.md)", "[matika/eight_precepts](eight_precepts.md)"]
    },
    "abstaining_from_intoxicants": {
        "title_en": "Abstaining from Intoxicants",
        "title_pali": "Surāmerayamajjapamādaṭṭhānā veramaṇī",
        "def_pali": "Surāmerayamajjapamādaṭṭhānā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from fermented and distilled liquors and intoxicants...",
        "description": "The fifth precept. It requires refraining from alcohol, drugs, or substances that impair mindfulness and cause heedlessness. It safeguards ethical integrity by preserving mental clarity.",
        "parents": ["five_precepts", "eight_precepts"],
        "suttas": ["[matika/five_precepts](five_precepts.md)", "[matika/eight_precepts](eight_precepts.md)"]
    },
    "abstaining_from_unchastity": {
        "title_en": "Abstaining from Unchastity",
        "title_pali": "Abrahmacariyā veramaṇī",
        "def_pali": "Abrahmacariyā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from unchastity...",
        "description": "The third precept on observance days and for monastics. It replaces the precept on sexual misconduct with a commitment to absolute celibacy (chastity), directing sexual energy toward spiritual purification.",
        "parents": ["eight_precepts"],
        "suttas": ["[matika/eight_precepts](eight_precepts.md)", "[mula/vinaya/patimokkha_bhikkhu](../mula/vinaya/patimokkha_bhikkhu.md)"]
    },
    "abstaining_from_eating_after_noon": {
        "title_en": "Abstaining from Eating After Noon",
        "title_pali": "Vikālabhojanā veramaṇī",
        "def_pali": "Vikālabhojanā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from eating at wrong times...",
        "description": "The sixth precept. It requires refraining from consuming solid food between solar noon and dawn. It reduces physical heaviness, supports meditation energy, and makes one easy to support.",
        "parents": ["eight_precepts"],
        "suttas": ["[matika/eight_precepts](eight_precepts.md)"]
    },
    "abstaining_from_entertainment_and_adornments": {
        "title_en": "Abstaining from Entertainment & Adornments",
        "title_pali": "Naccagītavāditavisūkadassanāmālāgandhavilepana...",
        "def_pali": "Naccagītavāditavisūkadassanāmālāgandhavilepanadhāraṇamaṇḍanavibhūsanaṭṭhānā veramaṇī...",
        "def_en": "I undertake the training rule to abstain from dancing, singing, music, shows, garlands, perfumes, cosmetics...",
        "description": "The seventh precept. It requires refraining from seeking sensory distraction through shows, music, and performance, and refraining from bodily vanity. It fosters simplicity, inward reflection, and content.",
        "parents": ["eight_precepts"],
        "suttas": ["[matika/eight_precepts](eight_precepts.md)"]
    },
    "abstaining_from_high_beds": {
        "title_en": "Abstaining from High Beds",
        "title_pali": "Uccāsayanamahāsayanā veramaṇī",
        "def_pali": "Uccāsayanamahāsayanā veramaṇīsikkhāpadaṃ samādiyāmi...",
        "def_en": "I undertake the training rule to abstain from high and luxurious beds...",
        "description": "The eighth precept. It requires refraining from sleeping on elevated, luxurious, or soft beds that encourage indulgence and sleepiness. It cultivates simplicity, mindfulness, and wakefulness.",
        "parents": ["eight_precepts"],
        "suttas": ["[matika/eight_precepts](eight_precepts.md)"]
    },

    # 5. Hindrances & Fetters
    "sensual_desire": {
        "title_en": "Sensual Desire",
        "title_pali": "Kāmacchanda / Kāmarāga",
        "def_pali": "Katamo ca, bhikkhave, kāmacchando? Vivicceva kāmehi...",
        "def_en": "And what, bhikkhus, is sensual desire? Secluded from sensual pleasures...",
        "description": "Kāmacchanda (or kāmarāga) is the desire, lust, and attraction for pleasant sights, sounds, smells, tastes, touches, and thoughts. It binds the mind to external objects, preventing concentration and tranquility.",
        "parents": ["five_hindrances", "ten_fetters"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "ill_will_or_hostility": {
        "title_en": "Ill Will / Hostility",
        "title_pali": "Vyāpāda / Paṭigha",
        "def_pali": "Vyāpādo ti: dosa-sahagato cetaso...",
        "def_en": "Ill will is: a state of mind accompanied by anger...",
        "description": "Vyāpāda (or paṭigha) is the aversion, anger, hostility, and resentment directed toward people, situations, or oneself. It burns the mind, preventing peace and clarity, and is countered by loving-kindness.",
        "parents": ["five_hindrances", "ten_fetters"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "sloth_and_torpor": {
        "title_en": "Sloth and Torpor",
        "title_pali": "Thīna-middha",
        "def_pali": "Thīnañca middhañca: thīnaṃ cittass'akalyatā, middhaṃ kāyassa...",
        "def_en": "Sloth and torpor: sloth is the sickness of mind, torpor is the sickness of body...",
        "description": "Thīna-middha is the dullness, sluggishness, and sleepiness of mind (sloth) and body (torpor). It manifests as mental fog and lack of energy, and is countered by arousing energy (*viriya*).",
        "parents": ["five_hindrances"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "restlessness_and_remorse": {
        "title_en": "Restlessness and Remorse",
        "title_pali": "Uddhacca-kukkucca",
        "def_pali": "Uddhacca-kukkuccanti: uddhaccaṃ cetaso avūpasamo, kukkuccaṃ...",
        "def_en": "Restlessness and remorse: restlessness is the unquiet of mind, remorse is regret...",
        "description": "Uddhacca-kukkucca is the combination of mental agitation, scattered thoughts (restlessness), and worry or guilt over past actions (remorse). It makes the mind jump from thought to thought, and is countered by tranquility (*passaddhi*).",
        "parents": ["five_hindrances", "ten_fetters"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "skeptical_doubt": {
        "title_en": "Skeptical Doubt",
        "title_pali": "Vicikicchā",
        "def_pali": "Vicikicchāti: kaṅkhā, kaṅkhāyanā, vimati...",
        "def_en": "Skeptical doubt is: doubting, hesitating, uncertainty...",
        "description": "Vicikicchā is the inability to decide, lack of conviction, and chronic indecision regarding the Buddha, Dhamma, Sangha, and the training. It paralyzes practice and is resolved by study, examination, and insight.",
        "parents": ["five_hindrances", "ten_fetters"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "identity_view": {
        "title_en": "Identity View / Self-view",
        "title_pali": "Sakkāyadiṭṭhi",
        "def_pali": "Idha, bhikkhave, assutavā puthujjanaṃ... rūpaṃ attato samanupassati...",
        "def_en": "Here, bhikkhus, an uninstructed worldling... regards form as self...",
        "description": "Sakkāyadiṭṭhi is the fundamental delusion that identifies one's selfhood with one or more of the five aggregates (e.g. regarding form, feeling, perception, choices, or consciousness as 'myself'). It is the first fetter cut at stream-entry.",
        "parents": ["ten_fetters"],
        "suttas": ["[SN 22.59: Anattalakkhaṇasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[MN 44: Cūḷavedallasutta](../mula/sutta/majjhima_nikaya/mn44.md)"]
    },
    "clinging_to_rites_and_rituals": {
        "title_en": "Clinging to Rites & Rituals",
        "title_pali": "Sīlabbataparāmāsa",
        "def_pali": "Iti sīlena... iti vatena suddhīti abhiveso...",
        "def_en": "The adherence to the belief that purity comes merely through rules... and vows...",
        "description": "Sīlabbataparāmāsa is the belief that liberation can be achieved simply by external rules, rituals, moral vows, or ascetic practices alone, without purifying the mind. It is abandoned at stream-entry.",
        "parents": ["ten_fetters"],
        "suttas": ["[MN 22: Alagaddūpamasutta](../mula/sutta/majjhima_nikaya/mn22.md)", "[matika/ten_fetters](ten_fetters.md)"]
    },
    "lust_for_material_existence": {
        "title_en": "Lust for Material Existence",
        "title_pali": "Rūparāga",
        "def_pali": "Rūpabhavesu chandarāgo...",
        "def_en": "Lust and desire for fine-material existences...",
        "description": "Rūparāga is the subtle attachment to rebirth in the fine-material Brahma realms, or attachment to the fine-material absorptions (the first four jhānas). It is a higher fetter abandoned only by an Arahant.",
        "parents": ["ten_fetters"],
        "suttas": ["[AN 9.36: Jhānasutta](../mula/sutta/anguttara_nikaya/an9_36.md)", "[matika/ten_fetters](ten_fetters.md)"]
    },
    "lust_for_immaterial_existence": {
        "title_en": "Lust for Immaterial Existence",
        "title_pali": "Arūparāga",
        "def_pali": "Arūpabhavesu chandarāgo...",
        "def_en": "Lust and desire for immaterial/formless existences...",
        "description": "Arūparāga is the attachment to rebirth in the formless realms, or attachment to the formless meditative attainments (infinite space, infinite consciousness, nothingness, neither-perception-nor-non-perception). It is cut by an Arahant.",
        "parents": ["ten_fetters"],
        "suttas": ["[AN 9.36: Jhānasutta](../mula/sutta/anguttara_nikaya/an9_36.md)", "[matika/ten_fetters](ten_fetters.md)"]
    },
    "conceit": {
        "title_en": "Conceit / Pride",
        "title_pali": "Māna",
        "def_pali": "Seyyohamasmīti vā... sadisohamasmīti vā... hīnohamasmīti vā...",
        "def_en": "The thought: 'I am better,' 'I am equal,' or 'I am worse'...",
        "description": "Māna is the lingering conceit of selfhood that compares oneself to others, manifesting as feelings of superiority, equality, or inferiority. It is a very deep defilement that persists until full enlightenment.",
        "parents": ["ten_fetters"],
        "suttas": ["[SN 22.95: Phenapiṇḍūpamasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/ten_fetters](ten_fetters.md)"]
    },

    # 6. Meditation / Awakening Factors
    "mindfulness": {
        "title_en": "Mindfulness",
        "title_pali": "Sati",
        "def_pali": "Satisambojjhaṅgo, satindriyaṃ, satibalaṃ...",
        "def_en": "The awakening factor of mindfulness, the faculty of mindfulness, the power of mindfulness...",
        "description": "Sati is the quality of steady, clear, and non-reactive attention. It recollectedly anchors the mind in the present moment, allowing it to monitor experience with clarity, and serves as the foundation for both tranquility and insight.",
        "parents": ["seven_awakening_factors", "five_spiritual_faculties", "five_powers"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[MN 118: Ānāpānasatisutta](../mula/sutta/majjhima_nikaya/mn118.md)"]
    },
    "investigation_of_phenomena": {
        "title_en": "Investigation of Phenomena",
        "title_pali": "Dhammavicaya",
        "def_pali": "Yo taṃ dhammaṃ paññāya vicināti pavicināti...",
        "def_en": "That which investigates, examines, and inspects that state with wisdom...",
        "description": "Dhammavicaya is the active, analytical aspect of wisdom. It investigates physical and mental states to see if they are wholesome or unwholesome, helpful or unhelpful, and discerns their characteristics of anicca, dukkha, and anattā.",
        "parents": ["seven_awakening_factors"],
        "suttas": ["[MN 118: Ānāpānasatisutta](../mula/sutta/majjhima_nikaya/mn118.md)", "[matika/seven_awakening_factors](seven_awakening_factors.md)"]
    },
    "energy": {
        "title_en": "Energy / Effort",
        "title_pali": "Viriya",
        "def_pali": "Viriyasambojjhaṅgo, viriyindriyaṃ, viriyabalaṃ...",
        "def_en": "The awakening factor of energy, the faculty of energy, the power of energy...",
        "description": "Viriya is spiritual energy, vigor, and determination. It drives the mind to overcome sloth and dullness, actively strives to cultivate wholesome states, and provides the strength required to sustain meditative practice.",
        "parents": ["seven_awakening_factors", "five_spiritual_faculties", "five_powers", "ten_perfections"],
        "suttas": ["[MN 118: Ānāpānasatisutta](../mula/sutta/majjhima_nikaya/mn118.md)", "[matika/four_right_exertions](four_right_exertions.md)"]
    },
    "rapture_or_joy": {
        "title_en": "Rapture / Joy",
        "title_pali": "Pīti",
        "def_pali": "Pītisambojjhaṅgo: pīti, pāmojjaṃ, hāso...",
        "def_en": "The awakening factor of rapture: rapture, gladness, laughter...",
        "description": "Pīti is the physical and mental rapture, joy, or thrill born of meditation. It arises when the mind is secluded from sensory distractions and unwholesome states, providing a pleasant interest that prevents restlessness.",
        "parents": ["seven_awakening_factors"],
        "suttas": ["[MN 118: Ānāpānasatisutta](../mula/sutta/majjhima_nikaya/mn118.md)", "[AN 5.28: Pañcaṅgikasutta](../mula/sutta/anguttara_nikaya/an5_28.md)"]
    },
    "tranquility": {
        "title_en": "Tranquility",
        "title_pali": "Passaddhi",
        "def_pali": "Kāyapassaddhi, cittapassaddhi...",
        "def_en": "Tranquility of body, tranquility of mind...",
        "description": "Passaddhi is the physical quietude and mental calm that succeeds joy. It eliminates physical tension (kāya-passaddhi) and mental restlessness (citta-passaddhi), preparing the mind for deep immersion/concentration.",
        "parents": ["seven_awakening_factors"],
        "suttas": ["[MN 118: Ānāpānasatisutta](../mula/sutta/majjhima_nikaya/mn118.md)", "[matika/seven_awakening_factors](seven_awakening_factors.md)"]
    },
    "immersion_or_concentration": {
        "title_en": "Immersion / Concentration",
        "title_pali": "Samādhi",
        "def_pali": "Samādhisambojjhaṅgo, samādhindriyaṃ, samādhibalaṃ...",
        "def_en": "The awakening factor of immersion, the faculty of immersion, the power of immersion...",
        "description": "Samādhi is the collectedness, stillness, and one-pointedness of mind. It unifies mental activity, stops wandering thoughts, and leads to the deep meditative absorptions (jhānas), stabilizing the mind for wisdom.",
        "parents": ["seven_awakening_factors", "five_spiritual_faculties", "five_powers"],
        "suttas": ["[DN 2: Sāmaññaphalasutta](../mula/sutta/digha_nikaya/dn2.md)", "[AN 5.28: Pañcaṅgikasutta](../mula/sutta/anguttara_nikaya/an5_28.md)"]
    },
    "equanimity": {
        "title_en": "Equanimity",
        "title_pali": "Upekkhā",
        "def_pali": "Upekkhāsambojjhaṅgo: tatramajjhattatā...",
        "def_en": "The awakening factor of equanimity: neutral balance...",
        "description": "Upekkhā is the mental quality of neutral balance, evenness, and freedom from attraction and aversion. It allows the mind to observe experience without reacting, providing the spaciousness required for ultimate insight.",
        "parents": ["seven_awakening_factors", "ten_perfections", "four_sublime_states"],
        "suttas": ["[MN 118: Ānāpānasatisutta](../mula/sutta/majjhima_nikaya/mn118.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "faith_or_conviction": {
        "title_en": "Faith / Conviction",
        "title_pali": "Saddhā",
        "def_pali": "Saddhindriyaṃ, saddhābalaṃ: tathāgatassa bodhiṃ saddahati...",
        "def_en": "The faculty of faith, the power of faith: one has faith in the awakening of the Tathāgata...",
        "description": "Saddhā is the confidence, trust, or conviction that arises from understanding the Dhamma. It is not blind belief, but the trust in the Buddha's awakening, the efficacy of kamma, and the path of training, which inspires effort.",
        "parents": ["five_spiritual_faculties", "five_powers"],
        "suttas": ["[SN 55: Sotāpattisaṃyutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/five_spiritual_faculties](five_spiritual_faculties.md)"]
    },
    "wisdom_or_discernment": {
        "title_en": "Wisdom / Discernment",
        "title_pali": "Paññā",
        "def_pali": "Paññindriyaṃ, paññābalaṃ: udayatthagāminiyā paññāya samannāgato...",
        "def_en": "The faculty of wisdom, the power of wisdom: one possesses wisdom regarding arising and passing away...",
        "description": "Paññā is the wisdom or discernment that understands things as they really are. It is defined as the understanding of arising and passing away, which leads to the complete destruction of suffering and the realization of Nibbāna.",
        "parents": ["five_spiritual_faculties", "five_powers", "ten_perfections"],
        "suttas": ["[MN 43: Mahāvedallasutta](../mula/sutta/majjhima_nikaya/mn43.md)", "[MN 44: Cūḷavedallasutta](../mula/sutta/majjhima_nikaya/mn44.md)"]
    },

    # 7. Three Refuges
    "buddha": {
        "title_en": "The Buddha",
        "title_pali": "Buddha",
        "def_pali": "Itipi so bhagavā arahaṃ sammāsambuddho...",
        "def_en": "Thus is the Blessed One: an arahant, a fully awakened one...",
        "description": "The Buddha is the historical teacher, Siddhattha Gotama, who discovered the path to Nibbāna through his own efforts and taught it out of compassion. He represents the teacher and the ultimate potential of human awakening.",
        "parents": ["three_refuges"],
        "suttas": ["[SN 55: Sotāpattisaṃyutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/three_refuges](three_refuges.md)"]
    },
    "dhamma": {
        "title_en": "The Dhamma",
        "title_pali": "Dhamma",
        "def_pali": "Svākkhāto bhagavatā dhammo sandiṭṭhiko akāliko...",
        "def_en": "The Dhamma is well-expounded by the Blessed One, visible here and now, timeless...",
        "description": "The Dhamma is the truth of reality, the natural laws of kamma and liberation, and the teachings expounded by the Buddha. It is described as visible here and now, inviting one to come and see (*ehipassiko*).",
        "parents": ["three_refuges"],
        "suttas": ["[SN 55: Sotāpattisaṃyutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/three_refuges](three_refuges.md)"]
    },
    "sangha": {
        "title_en": "The Sangha",
        "title_pali": "Sangha",
        "def_pali": "Supaṭipanno bhagavato sāvakasaṅgho...",
        "def_en": "The community of the Blessed One's disciples has practiced well...",
        "description": "The Sangha is the community of practitioners. Broadly, it refers to the monastic order, and specifically, to the Ariya-Sangha (noble disciples who have attained one of the four stages of stream-entry, once-returning, non-returning, or Arahantship).",
        "parents": ["three_refuges"],
        "suttas": ["[SN 55: Sotāpattisaṃyutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/three_refuges](three_refuges.md)"]
    },

    # 8. Perfections & Sublime States
    "generosity": {
        "title_en": "Generosity",
        "title_pali": "Dāna",
        "def_pali": "Dānapāramī: datvā ca pariccajitvā ca...",
        "def_en": "The perfection of generosity: giving and relinquishing...",
        "description": "Dāna is the practice of giving, generosity, and sharing. It counters the root of greed and attachment, cultivates selflessness, and supports the Sangha and those in need. It is the first of the ten perfections.",
        "parents": ["ten_perfections"],
        "suttas": ["[AN 10.60: Girimānandasutta](../mula/sutta/majjhima_nikaya/an10_60.md)", "[matika/ten_perfections](ten_perfections.md)"]
    },
    "virtue": {
        "title_en": "Virtue / Ethical Conduct",
        "title_pali": "Sīla",
        "def_pali": "Sīlapāramī: kāyikavācasikasammācāro...",
        "def_en": "The perfection of virtue: right bodily and verbal conduct...",
        "description": "Sīla is ethical conduct, virtue, and moral discipline. It involves guarding one's physical and verbal actions to prevent harm to others and ourselves, establishing the stability required for meditation.",
        "parents": ["ten_perfections"],
        "suttas": ["[matika/five_precepts](five_precepts.md)", "[matika/eight_precepts](eight_precepts.md)"]
    },
    "renunciation": {
        "title_en": "Renunciation",
        "title_pali": "Nekkhamma",
        "def_pali": "Nekkhammapāramī: kāmaṃ pahāya nekkhammaṃ...",
        "def_en": "The perfection of renunciation: abandoning sensuality...",
        "description": "Nekkhamma is the perfection of renunciation and letting go. It is the act of stepping away from sensual pursuits and worldly attachments, finding freedom in simplicity, solitude, and meditation.",
        "parents": ["ten_perfections"],
        "suttas": ["[MN 19: Dvedhāvitakkasutta](../mula/sutta/majjhima_nikaya/mn19.md)", "[matika/right_intention](right_intention.md)"]
    },
    "patience_or_forbearance": {
        "title_en": "Patience / Forbearance",
        "title_pali": "Khanti",
        "def_pali": "Khantipāramī: khamano, adhivāsetā...",
        "def_en": "The perfection of patience: enduring and forbearing...",
        "description": "Khanti is patience, tolerance, and forbearance. It is the capacity to endure heat, cold, hunger, pain, insults, and harsh words without reacting in anger or losing one's peace of mind.",
        "parents": ["ten_perfections"],
        "suttas": ["[matika/ten_perfections](ten_perfections.md)"]
    },
    "truthfulness": {
        "title_en": "Truthfulness",
        "title_pali": "Sacca",
        "def_pali": "Saccapāramī: saccavādī, saccasandho...",
        "def_en": "The perfection of truthfulness: speaking truth, committing to truth...",
        "description": "Sacca is the perfection of truthfulness, honesty, and alignment with reality. It is the commitment to speak only what is true and beneficial, and to align one's life with the Truth of Dhamma.",
        "parents": ["ten_perfections"],
        "suttas": ["[matika/right_speech](right_speech.md)", "[matika/ten_perfections](ten_perfections.md)"]
    },
    "determination": {
        "title_en": "Determination / Resolve",
        "title_pali": "Adhiṭṭhāna",
        "def_pali": "Adhiṭṭhānapāramī: acalādhiṭṭhānaṃ...",
        "def_en": "The perfection of determination: immovable resolve...",
        "description": "Adhiṭṭhāna is determination, resolution, and firm purpose. It is the power of resolve that sustains a practitioner through obstacles and long periods of training without wavering or giving up.",
        "parents": ["ten_perfections"],
        "suttas": ["[matika/ten_perfections](ten_perfections.md)"]
    },
    "loving_kindness": {
        "title_en": "Loving-kindness",
        "title_pali": "Mettā",
        "def_pali": "Sabbe sattā sukhino va khemino hontu...",
        "def_en": "May all beings be happy and secure...",
        "description": "Mettā is loving-kindness, benevolence, and universal goodwill. It is the wish for all beings to be happy, safe, and free from inner and outer harm. It counters anger, hatred, and resentment.",
        "parents": ["ten_perfections", "four_sublime_states"],
        "suttas": ["[AN 11.15: Karaṇīyamettāsutta](../mula/sutta/anguttara_nikaya/an11_15.md)", "[DN 13: Tevijjasutta](../mula/sutta/digha_nikaya/dn13.md)"]
    },
    "compassion": {
        "title_en": "Compassion",
        "title_pali": "Karuṇā",
        "def_pali": "Karuṇūpekkhā, karuṇāyanā: paradukkhe sati kampanaṃ...",
        "def_en": "Compassion: trembling at the suffering of others...",
        "description": "Karuṇā is compassion. It is the quality of heart that trembles in response to the suffering of others, wishing for them to be free from pain and distress. It counters cruelty and cold indifference.",
        "parents": ["four_sublime_states"],
        "suttas": ["[DN 13: Tevijjasutta](../mula/sutta/digha_nikaya/dn13.md)", "[matika/four_sublime_states](four_sublime_states.md)"]
    },
    "appreciative_joy": {
        "title_en": "Appreciative / Sympathetic Joy",
        "title_pali": "Muditā",
        "def_pali": "Modanā, muditā, pramodo: parasampattiyā pamodanaṃ...",
        "def_en": "Rejoicing, sympathetic joy: gladness at the success of others...",
        "description": "Muditā is appreciative or sympathetic joy. It is the capacity to rejoice in the happiness, achievements, and success of other living beings, serving as the direct antidote to envy and jealousy.",
        "parents": ["four_sublime_states"],
        "suttas": ["[DN 13: Tevijjasutta](../mula/sutta/digha_nikaya/dn13.md)", "[matika/four_sublime_states](four_sublime_states.md)"]
    },

    # 9. Four Foundations of Mindfulness (Mindfulness Targets)
    "contemplation_of_body": {
        "title_en": "Contemplation of the Body",
        "title_pali": "Kāyānupassanā",
        "def_pali": "Kāye kāyānupassī viharati ātāpī sampajāno...",
        "def_en": "He dwells contemplating the body in the body, ardent...",
        "description": "Kāyānupassanā is the first foundation of mindfulness. It directs attention to the physical body: observing the breath, the postures (walking, standing, sitting, lying), bodily elements, and parts of the body, breaking the illusion of bodily beauty and permanence.",
        "parents": ["four_foundations_of_mindfulness"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[MN 119: Kāyagatāsatisutta](../mula/sutta/majjhima_nikaya/mn119.md)"]
    },
    "contemplation_of_feelings": {
        "title_en": "Contemplation of Feelings",
        "title_pali": "Vedanānupassanā",
        "def_pali": "Vedanāsu vedanānupassī viharati ātāpī sampajāno...",
        "def_en": "He dwells contemplating feelings in feelings, ardent...",
        "description": "Vedanānupassanā is the second foundation. It observes the hedonic tone of experience: pleasant, painful, or neutral sensations as they hit the senses, revealing their impermanence and preventing reactive craving/aversion.",
        "parents": ["four_foundations_of_mindfulness"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "contemplation_of_mind": {
        "title_en": "Contemplation of the Mind",
        "title_pali": "Cittānupassanā",
        "def_pali": "Citte cittānupassī viharati ātāpī sampajāno...",
        "def_en": "He dwells contemplating mind in mind, ardent...",
        "description": "Cittānupassanā is the third foundation. It observes the quality of the mind, identifying if the mind is currently with or without greed, anger, delusion, concentration, distraction, or liberation.",
        "parents": ["four_foundations_of_mindfulness"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },
    "contemplation_of_phenomena": {
        "title_en": "Contemplation of Phenomena",
        "title_pali": "Dhammānupassanā",
        "def_pali": "Dhammesu dhammānupassī viharati ātāpī sampajāno...",
        "def_en": "He dwells contemplating phenomena in phenomena, ardent...",
        "description": "Dhammānupassanā is the fourth foundation. It contemplates mental categories and laws of cause-and-effect: the five hindrances, five aggregates, six sense bases, seven awakening factors, and the Four Noble Truths.",
        "parents": ["four_foundations_of_mindfulness"],
        "suttas": ["[MN 10: Satipaṭṭhānasutta](../mula/sutta/majjhima_nikaya/mn10.md)", "[DN 22: Mahāsatipaṭṭhānasutta](../mula/sutta/digha_nikaya/dn22.md)"]
    },

    # 10. Three Unwholesome Roots
    "greed": {
        "title_en": "Greed / Desire",
        "title_pali": "Lobha",
        "def_pali": "Katamo ca, bhikkhave, lobho? Yo cittassa rāgo...",
        "def_en": "And what, bhikkhus, is greed? The lust of the mind...",
        "description": "Lobha is greed, lust, and attachment. It is the mental state of pulling towards, grasping, and demanding experiences or possessions, keeping the mind agitated and bound to the cycle of craving.",
        "parents": ["three_unwholesome_roots"],
        "suttas": ["[MN 9: Sammādiṭṭhisutta](../mula/sutta/majjhima_nikaya/mn9.md)", "[matika/three_unwholesome_roots](three_unwholesome_roots.md)"]
    },
    "hatred": {
        "title_en": "Hatred / Anger",
        "title_pali": "Dosa",
        "def_pali": "Katamo ca, bhikkhave, doso? Yo cittassa vyāpādo...",
        "def_en": "And what, bhikkhus, is hatred? The ill will of the mind...",
        "description": "Dosa is hatred, anger, and aversion. It is the mental state of pushing away, rejecting, and showing hostility toward experiences or people, acting as the root of ill will and conflict.",
        "parents": ["three_unwholesome_roots"],
        "suttas": ["[MN 9: Sammādiṭṭhisutta](../mula/sutta/majjhima_nikaya/mn9.md)", "[matika/three_unwholesome_roots](three_unwholesome_roots.md)"]
    },
    "delusion": {
        "title_en": "Delusion / Ignorance",
        "title_pali": "Moha",
        "def_pali": "Katamo ca, bhikkhave, moho? Yaṃ aññāṇaṃ...",
        "def_en": "And what, bhikkhus, is delusion? The ignorance...",
        "description": "Moha is delusion and ignorance. It is the mental state of confusion and lack of clarity, which misperceives reality and forms the foundation upon which greed and hatred can arise.",
        "parents": ["three_unwholesome_roots"],
        "suttas": ["[MN 9: Sammādiṭṭhisutta](../mula/sutta/majjhima_nikaya/mn9.md)", "[matika/three_unwholesome_roots](three_unwholesome_roots.md)"]
    },

    # 11. Four Right Exertions
    "effort_to_prevent": {
        "title_en": "Effort to Prevent",
        "title_pali": "Saṃvara",
        "def_pali": "Anuppannānaṃ pāpakānaṃ akusalānaṃ dhammānaṃ anuppādāya...",
        "def_en": "To prevent the arising of unarisen evil unwholesome states...",
        "description": "The first right exertion. It involves guarding the sense doors (eyes, ears, etc.) to prevent unwholesome thoughts, desires, and distractions from arising in the mind.",
        "parents": ["four_right_exertions"],
        "suttas": ["[matika/four_right_exertions](four_right_exertions.md)", "[matika/right_effort](right_effort.md)"]
    },
    "effort_to_abandon": {
        "title_en": "Effort to Abandon",
        "title_pali": "Pahāna",
        "def_pali": "Uppannānaṃ pāpakānaṃ akusalānaṃ dhammānaṃ pahānāya...",
        "def_en": "To abandon arisen evil unwholesome states...",
        "description": "The second right exertion. It involves actively letting go, dissolving, and banishing unwholesome states (like sensuality, anger, or worry) that have already arisen in the mind.",
        "parents": ["four_right_exertions"],
        "suttas": ["[MN 20: Vitakkasaṇṭhānasutta](../mula/sutta/majjhima_nikaya/mn20.md)", "[matika/right_effort](right_effort.md)"]
    },
    "effort_to_develop": {
        "title_en": "Effort to Develop",
        "title_pali": "Bhāvanā",
        "def_pali": "Anuppannānaṃ kusalānaṃ dhammānaṃ uppādāya...",
        "def_en": "To bring about the arising of unarisen wholesome states...",
        "description": "The third right exertion. It involves cultivating and initiating wholesome qualities (like the seven awakening factors and concentration) that have not yet arisen in the mind.",
        "parents": ["four_right_exertions"],
        "suttas": ["[matika/four_right_exertions](four_right_exertions.md)", "[matika/right_effort](right_effort.md)"]
    },
    "effort_to_maintain": {
        "title_en": "Effort to Maintain",
        "title_pali": "Anurakkhaṇā",
        "def_pali": "Uppannānaṃ kusalānaṃ dhammānaṃ ṭhitiyā...",
        "def_en": "To maintain arisen wholesome states, to prevent their ruin...",
        "description": "The fourth right exertion. It involves protecting, increasing, and bringing to full maturity the wholesome states that are already present in the mind, keeping them active.",
        "parents": ["four_right_exertions"],
        "suttas": ["[matika/four_right_exertions](four_right_exertions.md)", "[matika/right_effort](right_effort.md)"]
    },

    # 12. Seven Purifications
    "purification_of_virtue": {
        "title_en": "Purification of Virtue",
        "title_pali": "Sīla-visuddhi",
        "def_pali": "Sīlavisuddhi kho pana... pātimokkhasaṃvarasīlaṃ...",
        "def_en": "Purification of virtue is... moral discipline according to monastic code...",
        "description": "The first purification. It is the refinement of moral behavior, restraint of the senses, and pure livelihood. It establishes the clean foundation upon which meditation can succeed.",
        "parents": ["seven_purifications"],
        "suttas": ["[matika/seven_purifications](seven_purifications.md)", "[mula/vinaya/patimokkha_bhikkhu](../mula/vinaya/patimokkha_bhikkhu.md)"]
    },
    "purification_of_mind": {
        "title_en": "Purification of Mind",
        "title_pali": "Citta-visuddhi",
        "def_pali": "Cittavisuddhi kho pana... upacārasamādhi appanāsamādhi...",
        "def_en": "Purification of mind is... access concentration and absorption concentration...",
        "description": "The second purification. It is the development of concentration and silencing of the five hindrances, achieved through access concentration (*upacāra*) and absorption concentration (*appanā* / jhānas).",
        "parents": ["seven_purifications"],
        "suttas": ["[DN 2: Sāmaññaphalasutta](../mula/sutta/digha_nikaya/dn2.md)", "[matika/seven_purifications](seven_purifications.md)"]
    },
    "purification_of_view": {
        "title_en": "Purification of View",
        "title_pali": "Diṭṭhi-visuddhi",
        "def_pali": "Diṭṭhivisuddhi kho pana... nāmarūpānaṃ yathābhūtaṃ dassanaṃ...",
        "def_en": "Purification of view is... seeing name and form as they really are...",
        "description": "The third purification. It is the direct seeing of name-and-form (*nāmarūpa*) as impermanent processes, stripping away the default view of a permanent self or soul.",
        "parents": ["seven_purifications"],
        "suttas": ["[SN 22.59: Anattalakkhaṇasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/seven_purifications](seven_purifications.md)"]
    },
    "purification_by_overcoming_doubt": {
        "title_en": "Purification by Overcoming Doubt",
        "title_pali": "Kaṅkhāvitaraṇa-visuddhi",
        "def_pali": "Kaṅkhāvitaraṇavisuddhi... nāmarūpānaṃ paccayapariggaha...",
        "def_en": "Purification by overcoming doubt... discerning the causes of name and form...",
        "description": "The fourth purification. It is the understanding of the causal relationships of dependent origination, seeing how name-and-form arise due to causes, which resolves all doubt regarding past, present, and future existences.",
        "parents": ["seven_purifications"],
        "suttas": ["[SN 12.2: Vibhaṅgasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/seven_purifications](seven_purifications.md)"]
    },
    "purification_by_knowledge_and_vision_of_path": {
        "title_en": "Purification by Knowledge & Vision of Path",
        "title_pali": "Maggāmaggañāṇadassana-visuddhi",
        "def_pali": "Maggāmaggañāṇadassana... maggāmaggañāṇa...",
        "def_en": "Knowledge and vision of what is path and what is not path...",
        "description": "The fifth purification. It is the discernment that distinguishes between the true path of insight and the corruptions of insight (such as attachment to light, joy, or tranquility arising during meditation).",
        "parents": ["seven_purifications"],
        "suttas": ["[matika/seven_purifications](seven_purifications.md)"]
    },
    "purification_by_knowledge_and_vision_of_way": {
        "title_en": "Purification by Knowledge & Vision of Way",
        "title_pali": "Paṭipadāñāṇadassana-visuddhi",
        "def_pali": "Paṭipadāñāṇadassana... navānupassanāñāṇānaṃ...",
        "def_en": "Knowledge and vision of the way... the nine insight knowledges...",
        "description": "The sixth purification. It is the development of the nine insight knowledges (such as knowledge of arising/passing, dissolution, fear, danger, disenchantment) that lead directly to the brink of liberation.",
        "parents": ["seven_purifications"],
        "suttas": ["[matika/seven_purifications](seven_purifications.md)"]
    },
    "purification_by_knowledge_and_vision": {
        "title_en": "Purification by Knowledge and Vision",
        "title_pali": "Ñāṇadassana-visuddhi",
        "def_pali": "Ñāṇadassana... catunnaṃ maggānaṃ ñāṇaṃ...",
        "def_en": "Knowledge and vision... knowledge of the four noble paths...",
        "description": "The seventh and final purification. It is the direct, supramundane knowledge of the four noble paths (stream-entry, once-returning, non-returning, Arahantship) which cuts the fetters and realizes Nibbāna.",
        "parents": ["seven_purifications"],
        "suttas": ["[SN 56.11: Dhammacakkappavattanasutta](../mula/sutta/samyutta_nikaya/INDEX.md)", "[matika/seven_purifications](seven_purifications.md)"]
    }
}

def generate_detail_files():
    print(f"Generating {len(FACTORS)} detail files in {MATIKA_DIR}...")
    for fid, data in FACTORS.items():
        filepath = os.path.join(MATIKA_DIR, f"{fid}.md")
        
        # Build Navigation headers (backlinks to parents)
        nav_items = ["[[../INDEX|Pali Canon Vault]]", "[[INDEX|Mātika]]"]
        for p in data["parents"]:
            # Format parent name nicely
            pname = p.replace("_", " ").title()
            nav_items.append(f"[[{p}|{pname}]]")
            
        nav_header = " / ".join(nav_items)
        
        # Build Sutta references links
        sutta_links = "\n".join([f"*   {s}" for s in data["suttas"]])
        
        content = f"""---
id: {fid}
title_pali: {data["title_pali"]}
type: matika
---

# {data["title_en"]} ({data["title_pali"]})

**Navigation**: {nav_header}

---

## Canonical Definition

> "{data["def_pali"]}"
> 
> *“{data["def_en"]}”*

---

## Detailed Description

{data["description"]}

---

## Sutta References

The following suttas and lists in the vault mention, describe, or analyze this factor:

{sutta_links}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("Detail files generation complete.")

def rewrite_parent_lists():
    # Mapping of parent lists to their new detailed link contents
    PARENT_UPDATES = {
        "four_noble_truths.md": (
            "## The List",
            """## The List

1. **[[suffering|Dukkha]]**  
   *Suffering / Unsatisfactoriness*
2. **[[origin_of_suffering|Samudaya]]**  
   *The origin / cause of suffering*
3. **[[cessation_of_suffering|Nirodha]]**  
   *The cessation / ending of suffering*
4. **[[path_to_cessation|Magga]]**  
   *The path of practice leading to the cessation of suffering*"""
        ),
        "three_marks.md": (
            "## The List",
            """## The List

1. **[[impermanence|Anicca]]**  
   *Impermanence / Inconstancy*
2. **[[suffering|Dukkha]]**  
   *Suffering / Unsatisfactoriness*
3. **[[non_self|Anattā]]**  
   *Non-self / Egolessness*"""
        ),
        "five_aggregates.md": (
            "## The List",
            """## The List

1. **[[form_or_matter|Rūpakkhandha]]**  
   *The aggregate of form / matter*
2. **[[feeling|Vedanākkhandha]]**  
   *The aggregate of feeling / sensation*
3. **[[perception|Saññākkhandha]]**  
   *The aggregate of perception / recognition*
4. **[[volitional_formations|Saṅkhārakkhandha]]**  
   *The aggregate of volitional formations / mental fabrications*
5. **[[consciousness_vinnana|Viññāṇakkhandha]]**  
   *The aggregate of consciousness / awareness*"""
        ),
        "dependent_origination.md": (
            "## The List",
            """## The List

1. **[[ignorance|Avijjā]]**  
   *Ignorance / Delusion*
2. **[[volitional_formations|Saṅkhārā]]**  
   *Volitional formations / Mental fabrications*
3. **[[consciousness_vinnana|Viññāṇa]]**  
   *Consciousness / Awareness*
4. **[[name_and_form|Nāmarūpa]]**  
   *Name-and-form / Mind-and-matter*
5. **[[six_sense_fields|Saḷāyatana]]**  
   *The six sense bases / fields*
6. **[[contact|Phassa]]**  
   *Sensory contact / Impingement*
7. **[[feeling|Vedanā]]**  
   *Feeling / Sensation*
8. **[[craving|Taṇhā]]**  
   *Craving / Thirst*
9. **[[clinging_or_grasping|Upādāna]]**  
   *Clinging / Grasping*
10. **[[existence_or_becoming|Bhava]]**  
    *Existence / Becoming*
11. **[[birth|Jāti]]**  
    *Birth / Re-entry*
12. **[[aging_and_death|Jarāmaraṇa]]**  
    *Aging and death / Dissolution*"""
        ),
        "five_precepts.md": (
            "## The List",
            """## The List

1. **[[abstaining_from_killing|Pāṇātipātā veramaṇī]]**  
   *Abstaining from taking life (killing)*
2. **[[abstaining_from_stealing|Adinnādānā veramaṇī]]**  
   *Abstaining from taking what is not given (stealing)*
3. **[[abstaining_from_sexual_misconduct|Kāmesumicchācārā veramaṇī]]**  
   *Abstaining from sexual misconduct*
4. **[[abstaining_from_false_speech|Musāvādā veramaṇī]]**  
   *Abstaining from false speech (lying)*
5. **[[abstaining_from_intoxicants|Surāmerayamajjapamādaṭṭhānā veramaṇī]]**  
   *Abstaining from fermented and distilled liquors and intoxicants*"""
        ),
        "five_hindrances.md": (
            "## The List",
            """## The List

1. **[[sensual_desire|Kāmacchanda]]**  
   *Sensual desire / Lust*
2. **[[ill_will_or_hostility|Vyāpāda]]**  
   *Ill will / Anger*
3. **[[sloth_and_torpor|Thīna-middha]]**  
   *Sloth and torpor / Sluggishness*
4. **[[restlessness_and_remorse|Uddhacca-kukkucca]]**  
   *Restlessness and remorse / Agitation*
5. **[[skeptical_doubt|Vicikicchā]]**  
   *Skeptical doubt / Indecision*"""
        ),
        "seven_awakening_factors.md": (
            "## The List",
            """## The List

1. **[[mindfulness|Satisambojjhaṅgo]]**  
   *Mindfulness*
2. **[[investigation_of_phenomena|Dhammavicayasambojjhaṅgo]]**  
   *Investigation of states / phenomena*
3. **[[energy|Viriyasambojjhaṅgo]]**  
   *Energy / Effort*
4. **[[rapture_or_joy|Pītisambojjhaṅgo]]**  
   *Rapture / Joy*
5. **[[tranquility|Passaddhisambojjhaṅgo]]**  
   *Tranquility / Calm*
6. **[[immersion_or_concentration|Samādhisambojjhaṅgo]]**  
   *Immersion / Concentration*
7. **[[equanimity|Upekkhāsambojjhaṅgo]]**  
   *Equanimity / Balance*"""
        ),
        "four_foundations_of_mindfulness.md": (
            "## The List",
            """## The List

1. **[[contemplation_of_body|Kāyānupassanā]]**  
   *Contemplation of the body*
2. **[[contemplation_of_feelings|Vedanānupassanā]]**  
   *Contemplation of feelings*
3. **[[contemplation_of_mind|Cittānupassanā]]**  
   *Contemplation of the mind*
4. **[[contemplation_of_phenomena|Dhammānupassanā]]**  
   *Contemplation of phenomena*"""
        ),
        "eight_precepts.md": (
            "## The List",
            """## The List

1. **[[abstaining_from_killing|Pāṇātipātā veramaṇī]]**  
   *Abstaining from taking life (killing)*
2. **[[abstaining_from_stealing|Adinnādānā veramaṇī]]**  
   *Abstaining from taking what is not given (stealing)*
3. **[[abstaining_from_unchastity|Abrahmacariya veramaṇī]]**  
   *Abstaining from unchastity (celibacy)*
4. **[[abstaining_from_false_speech|Musāvādā veramaṇī]]**  
   *Abstaining from false speech (lying)*
5. **[[abstaining_from_intoxicants|Surāmerayamajjapamādaṭṭhānā veramaṇī]]**  
   *Abstaining from fermented and distilled liquors and intoxicants*
6. **[[abstaining_from_eating_after_noon|Vikālabhojanā veramaṇī]]**  
   *Abstaining from eating at wrong times (after noon)*
7. **[[abstaining_from_entertainment_and_adornments|Naccagītavāditavisūkadassanāmālāgandhavilepanadhāraṇamaṇḍanavibhūsanaṭṭhānā veramaṇī]]**  
   *Abstaining from dancing, music, shows, perfumes, and cosmetics*
8. **[[abstaining_from_high_beds|Uccāsayanamahāsayanā veramaṇī]]**  
   *Abstaining from high and luxurious beds*"""
        ),
        "three_refuges.md": (
            "## The List",
            """## The List

1. **[[buddha|Buddhaṃ saraṇaṃ gacchāmi.]]**  
   *I go to the Buddha for refuge.*
2. **[[dhamma|Dhammaṃ saraṇaṃ gacchāmi.]]**  
   *I go to the Dhamma for refuge.*
3. **[[sangha|Saṅghaṃ saraṇaṃ gacchāmi.]]**  
   *I go to the Saṅgha for refuge.*"""
        ),
        "ten_perfections.md": (
            "## The List",
            """## The List

1. **[[generosity|Dānapāramī]]** — *Generosity / Giving*
2. **[[virtue|Sīlapāramī]]** — *Virtue / Ethical Conduct*
3. **[[renunciation|Nekkhammapāramī]]** — *Renunciation / Letting go*
4. **[[wisdom_or_discernment|Paññāpāramī]]** — *Wisdom / Insight*
5. **[[energy|Viriyapāramī]]** — *Energy / Effort*
6. **[[patience_or_forbearance|Khantipāramī]]** — *Patience / Tolerance*
7. **[[truthfulness|Saccapāramī]]** — *Truthfulness / Honesty*
8. **[[determination|Adhiṭṭhānapāramī]]** — *Determination / Resolve*
9. **[[loving_kindness|Mettāpāramī]]** — *Loving-kindness / Benevolence*
10. **[[equanimity|Upekkhāpāramī]]** — *Equanimity / Neutrality*"""
        ),
        "four_sublime_states.md": (
            "## The List",
            """## The List

1. **[[loving_kindness|Mettā]]**  
   *Loving-kindness / Universal goodwill*
2. **[[compassion|Karuṇā]]**  
   *Compassion / Empathy with suffering*
3. **[[appreciative_joy|Muditā]]**  
   *Appreciative joy / Joy at others' success*
4. **[[equanimity|Upekkhā]]**  
   *Equanimity / Mental balance*"""
        ),
        "five_spiritual_faculties.md": (
            "## The List",
            """## The List

1. **[[faith_or_conviction|Saddhindriya]]**  
   *The faculty of faith / conviction*
2. **[[energy|Viriyindriya]]**  
   *The faculty of energy / effort*
3. **[[mindfulness|Satindriya]]**  
   *The faculty of mindfulness*
4. **[[immersion_or_concentration|Samādhindriya]]**  
   *The faculty of concentration / immersion*
5. **[[wisdom_or_discernment|Paññindriya]]**  
   *The faculty of wisdom / discernment*"""
        ),
        "three_unwholesome_roots.md": (
            "## The List",
            """## The List

1. **[[greed|Lobha]]**  
   *Greed / Attachment / Lust*
2. **[[hatred|Dosa]]**  
   *Hatred / Anger / Aversion*
3. **[[delusion|Moha]]**  
   *Delusion / Ignorance*"""
        ),
        "four_right_exertions.md": (
            "## The List",
            """## The List

1. **[[effort_to_prevent|Saṃvaro]]** — *The effort to prevent*
2. **[[effort_to_abandon|Pahānaṃ]]** — *The effort to abandon*
3. **[[effort_to_develop|Bhāvanā]]** — *The effort to develop*
4. **[[effort_to_maintain|Anurakkhaṇā]]** — *The effort to maintain*"""
        ),
        "ten_fetters.md": (
            "## 1. Suttanta List (Primary)",
            """## The List

1. **[[identity_view|Sakkāyadiṭṭhi]]** — *Identity view / Self-view*
2. **[[skeptical_doubt|Vicikicchā]]** — *Skeptical doubt / Indecision*
3. **[[clinging_to_rites_and_rituals|Sīlabbataparāmāso]]** — *Clinging to rules and rituals*
4. **[[sensual_desire|Kāmarāgo]]** — *Sensual desire / Lust*
5. **[[ill_will_or_hostility|Paṭigho]]** — *Ill will / Anger / Aversion*
6. **[[lust_for_material_existence|Rūparāgo]]** — *Lust for material existence (Brahma realms)*
7. **[[lust_for_immaterial_existence|Arūparāgo]]** — *Lust for immaterial existence (Formless realms)*
8. **[[conceit|Māno]]** — *Conceit / Pride*
9. **[[restlessness_and_remorse|Uddhaccaṃ]]** — *Restlessness / Agitation*
10. **[[ignorance|Avijjā]]** — *Ignorance / Delusion*"""
        ),
        "seven_purifications.md": (
            "## 1. The List",
            """## The List

1. **[[purification_of_virtue|Sīlavisuddhi]]** — *Purification of virtue*
2. **[[purification_of_mind|Cittavisuddhi]]** — *Purification of mind*
3. **[[purification_of_view|Diṭṭhivisuddhi]]** — *Purification of view*
4. **[[purification_by_overcoming_doubt|Kaṅkhāvitaraṇavisuddhi]]** — *Purification by overcoming doubt*
5. **[[purification_by_knowledge_and_vision_of_path|Maggāmaggañāṇadassanavisuddhi]]** — *Purification by knowledge and vision of what is path and not-path*
6. **[[purification_by_knowledge_and_vision_of_way|Paṭipadāñāṇadassanavisuddhi]]** — *Purification by knowledge and vision of the way*
7. **[[purification_by_knowledge_and_vision|Ñāṇadassanavisuddhi]]** — *Purification by knowledge and vision*"""
        ),
        "five_powers.md": (
            "## The List",
            """## The List

1. **[[faith_or_conviction|Saddhābala]]**  
   *The power of faith / conviction*
2. **[[energy|Viriyabala]]**  
   *The power of energy / effort*
3. **[[mindfulness|Satibala]]**  
   *The power of mindfulness*
4. **[[immersion_or_concentration|Samādhibala]]**  
   *The power of concentration / immersion*
5. **[[wisdom_or_discernment|Paññābala]]**  
   *The power of wisdom / discernment*"""
        )
    }
    
    print(f"Updating {len(PARENT_UPDATES)} parent files...")
    for filename, (search_header, new_list) in PARENT_UPDATES.items():
        filepath = os.path.join(MATIKA_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Warning: parent file {filepath} not found.")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse and replace the list section
        # We search from the search_header to the next section or references
        # Since the list is bounded by the search_header and "## Related Lists" or "## Canonical References",
        # we can use a clean split and replace logic
        
        # Let's match from the specified search_header to the next heading starting with "##" or "---"
        escaped_header = re.escape(search_header)
        pattern = re.compile(rf"{escaped_header}.*?(?=##|---|\Z)", re.DOTALL)
        
        if pattern.search(content):
            new_content = pattern.sub(new_list + "\n\n", content)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully updated list in {filename}")
        else:
            print(f"Error: could not find list section in {filename} using '{search_header}'")

if __name__ == "__main__":
    generate_detail_files()
    rewrite_parent_lists()
    print("Mātika detailed factors expansion complete.")
