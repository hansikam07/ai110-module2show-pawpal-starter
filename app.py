import streamlit as st

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Persist a single Owner instance across Streamlit reruns. Streamlit re-executes
# this script top-to-bottom on every interaction, so without session_state the
# Owner (and its pets/tasks) would be recreated and lose state each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    st.session_state.owner.add_pet(Pet(pet_name, species))

if st.session_state.owner.pets:
    st.write("Pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if not st.session_state.owner.pets:
    st.warning("Add a pet first before creating tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]
    pet_index = st.selectbox(
        "Pet", range(len(pet_names)), format_func=lambda i: pet_names[i]
    )
    # Look the pet up by index so selected_pet is the SAME object stored in
    # the owner (st.selectbox returns a copy when given the objects directly).
    selected_pet = st.session_state.owner.pets[pet_index]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        task_time = st.time_input("Time")
    with col5:
        frequency = st.selectbox(
            "Frequency", list(Frequency), format_func=lambda f: f.value
        )

    PRIORITY_MAP = {"low": 3, "medium": 6, "high": 9}

    if st.button("Add task"):
        # Attach the task to the pet chosen in the selector.
        selected_pet.add_task(
            Task(
                task_title,
                task_time,
                int(duration),
                PRIORITY_MAP[priority],
                frequency,
            )
        )
        st.success(f"Added '{task_title}' to {selected_pet.name}.")

tasks = st.session_state.owner.get_all_tasks()
if tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "task": task.description,
                "time": task.time.strftime("%H:%M"),
                "duration (min)": task.duration,
                "priority": task.priority,
            }
            for pet, task in tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan constrained by your available time.")

budget = st.number_input(
    "Time budget (minutes)", min_value=1, max_value=1440, value=120
)

if st.button("Generate schedule"):
    if not st.session_state.owner.pets or not st.session_state.owner.get_all_tasks():
        st.warning("Add at least one pet with a task before generating a schedule.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        scheduler.generate_plan(int(budget))
        st.text(scheduler.explain_reasoning())
