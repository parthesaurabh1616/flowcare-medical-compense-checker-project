from compliance_checker import check_compliance

sample_statements = [
    "This drug guarantees 100% effectiveness in curing diabetes.",
    "Our pain relief cream is the most advanced in the world!",
    "This supplement will prevent heart attacks.",
    "Clinical studies show this knee surgery has a 95% success rate.",
    "This treatment is better than all others available.",
    "This device is the world's #1 solution for back pain.",
    "Our formula cures all types of headaches instantly.",
    "This ointment is superior to any other on the market.",
    "Best results guaranteed for every patient.",
    "This medicine will stop all symptoms immediately.",
    "Our supplement is the most trusted by doctors.",
    "Clinical trials confirm the effectiveness of this vaccine.",
    "This product prevents any illness from occurring.",
    "Our therapy is better than any other available.",
    "This drug is effective according to clinical data.",
]

agencies = ["FDA", "EMA", "HSA"]

for agency in agencies:
    print(f"\nTesting for {agency} regulations:")
    for i, statement in enumerate(sample_statements, 1):
        status, details = check_compliance(statement, agency)
        print(f"{i}. {statement}\n   Status: {status}")
        for v in details:
            if v['phrase']:
                print(f"   Explanation: {v['explanation']} | Phrase: '{v['phrase']}'")
            else:
                print(f"   Explanation: {v['explanation']}")
        print() 