import openai as OPENAI
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Your incident data built right into the code
incidents_data = [
    {'id': 1, 'type': 'Turbulence Injury', 'severity': 'High', 'date': '2025-02-03', 'location': 'Ground Handling', 'description': 'During baggage unloading'},
    {'id': 2, 'type': 'Near Miss (Ground)', 'severity': 'Critical', 'date': '2025-01-24', 'location': 'Cabin Crew', 'description': 'Pushback tractor cleared the aircraft without final confirmation'},
    {'id': 3, 'type': 'Hydraulic Failure', 'severity': 'Medium', 'date': '2025-04-27', 'location': 'Cabin Crew', 'description': 'Flight crew reported a loss of pressure in hydraulic system B during final approach. Landing was uneventful using alternate systems.'},
    {'id': 4, 'type': 'Bird Strike', 'severity': 'Medium', 'date': '2025-06-11', 'location': 'Security', 'description': 'Bird strike occurred on takeoff roll. Post-flight inspection revealed minor denting on the radome. No system malfunctions.'},
    {'id': 5, 'type': 'Navigation Error', 'severity': 'Low', 'date': '2025-05-15', 'location': 'Security', 'description': 'Aircraft taxied onto a non-assigned taxiway after landing due to a misread sign. Ground control provided corrective instructions.'},
    {'id': 6, 'type': 'Hydraulic Failure', 'severity': 'Low', 'date': '2025-07-03', 'location': 'Ground Handling', 'description': 'Minor hydraulic leak identified during pre-flight servicing from a loose connector. Repaired and system checked.'},
    {'id': 7, 'type': 'Runway Excursion', 'severity': 'High', 'date': '2025-09-19', 'location': 'Flight Operations', 'description': 'Aircraft veered off the taxiway onto soft grass during heavy rainfall. No injuries or damage. Tug required for recovery.'},
    {'id': 8, 'type': 'Turbulence Injury', 'severity': 'Low', 'date': '2025-02-07', 'location': 'Ground Handling', 'description': 'Passenger reported minor neck pain after encountering light turbulence during cruise. Attended to by cabin crew.'},
    {'id': 9, 'type': 'Hydraulic Failure', 'severity': 'Critical', 'date': '2025-03-26', 'location': 'Cabin Crew', 'description': 'Complete failure of hydraulic system A during pre-flight checks. Aircraft taken out of service for major maintenance.'},
    {'id': 10, 'type': 'Turbulence Injury', 'severity': 'Low', 'date': '2025-06-29', 'location': 'Ground Handling', 'description': 'Cabin crew member stumbled during beverage service due to clear-air turbulence'},
    {'id': 11, 'type': 'Bird Strike', 'severity': 'High', 'date': '2025-03-31', 'location': 'Security', 'description': 'Multiple bird strikes on final approach caused damage to both engine cowlings. Emergency inspection performed after landing.'},
    {'id': 12, 'type': 'Near Miss (Air)', 'severity': 'Medium', 'date': '2025-08-18', 'location': 'Administration', 'description': 'ATC issued a traffic advisory; two aircraft on converging courses were at same altitude. Both pilots initiated climb/descent per TCAS RA.'},
    {'id': 13, 'type': 'Turbulence Injury', 'severity': 'Low', 'date': '2025-04-10', 'location': 'Engineering', 'description': 'Engineer in the maintenance bay was struck on the head by a tool dislodged from an overhead panel due to vibration.'},
    {'id': 14, 'type': 'Passenger Misconduct', 'severity': 'High', 'date': '2025-07-30', 'location': 'Flight Operations', 'description': 'Passenger became physically aggressive towards cabin crew after being denied alcohol. Restrained with flex-cuffs with pilot assistance.'},
    {'id': 15, 'type': 'Navigation Error', 'severity': 'High', 'date': '2025-03-21', 'location': 'Cabin Crew', 'description': 'Cabin crew inadvertently armed the emergency slide while preparing the doors for arrival. Slide deployed at the gate.'},
    {'id': 16, 'type': 'Navigation Error', 'severity': 'High', 'date': '2025-07-20', 'location': 'Administration', 'description': 'Incorrect flight plan data entered into system caused a significant route deviation. Corrected en-route by ATC.'},
    {'id': 17, 'type': 'FOD (Foreign Object Debris)', 'severity': 'High', 'date': '2025-03-02', 'location': 'Cabin Crew', 'description': "Passenger's laptop battery caught fire and smoked during boarding. Extinguished with onboard fire extinguisher."},
    {'id': 18, 'type': 'Weather Diversion', 'severity': 'High', 'date': '2025-03-15', 'location': 'Ground Handling', 'description': 'Severe thunderstorm at destination required diversion to alternate airport. Low fuel state declared; landed safely.'},
    {'id': 19, 'type': 'Passenger Misconduct', 'severity': 'High', 'date': '2025-09-17', 'location': 'Engineering', 'description': 'Passenger attempted to force open a cabin door during flight. Subdued by other passengers and crew.'},
    {'id': 20, 'type': 'Weather Diversion', 'severity': 'Low', 'date': '2025-07-05', 'location': 'Ground Handling', 'description': 'Flight diverted to alternate due to fog. Ground handling services were delayed at the unscheduled airport.'},
    {'id': 21, 'type': 'Runway Excursion', 'severity': 'Critical', 'date': '2025-03-19', 'location': 'Administration', 'description': 'Aircraft overran the wet runway by 50 feet during landing. No injuries. Aircraft stuck in soft ground.'},
    {'id': 22, 'type': 'Unauthorized Entry', 'severity': 'Low', 'date': '2025-01-10', 'location': 'Administration', 'description': 'Contractor accessed the Operations floor without proper escort. Escorted out after verification.'},
    {'id': 23, 'type': 'Medical Emergency', 'severity': 'Low', 'date': '2025-08-11', 'location': 'Flight Operations', 'description': 'Passenger fainted due to low blood sugar. Administered oxygen and sugary drink. Passenger recovered.'},
    {'id': 24, 'type': 'Near Miss (Air)', 'severity': 'Low', 'date': '2025-07-26', 'location': 'Administration', 'description': 'Two aircraft on parallel taxi paths came within 200 feet laterally. Both stopped and confirmed positions with ground control.'},
    {'id': 25, 'type': 'Passenger Misconduct', 'severity': 'Low', 'date': '2025-02-19', 'location': 'Engineering', 'description': 'Passenger refused to turn off portable electronic device during takeoff. Device confiscated until landing.'},
    {'id': 26, 'type': 'Navigation Error', 'severity': 'Low', 'date': '2025-08-27', 'location': 'Engineering', 'description': 'Incorrect database cycle loaded into the FMS'},
    {'id': 27, 'type': 'Hydraulic Failure', 'severity': 'Medium', 'date': '2025-08-25', 'location': 'Ground Handling', 'description': 'Hydraulic reservoir found low during transit check. Suspected leak. Engineering inspection requested.'},
    {'id': 28, 'type': 'Weather Diversion', 'severity': 'Critical', 'date': '2025-07-27', 'location': 'Ground Handling', 'description': 'Diversion due to hurricane closure. Airport infrastructure overwhelmed'},
    {'id': 29, 'type': 'Hydraulic Failure', 'severity': 'Critical', 'date': '2025-02-22', 'location': 'Engineering', 'description': 'Catastrophic hydraulic failure during gear retraction. Emergency landing performed with alternate gear extension.'},
    {'id': 30, 'type': 'Navigation Error', 'severity': 'Low', 'date': '2025-08-18', 'location': 'Administration', 'description': 'Software glitch in flight planning system suggested an incorrect optimum altitude. Caught by flight crew during review.'},
    {'id': 31, 'type': 'Medical Emergency', 'severity': 'High', 'date': '2025-05-20', 'location': 'Administration', 'description': 'Passenger suffered a suspected heart attack mid-flight. Emergency medical services met the aircraft on arrival.'},
    {'id': 32, 'type': 'FOD (Foreign Object Debris)', 'severity': 'Medium', 'date': '2025-01-27', 'location': 'Flight Operations', 'description': 'Maintenance found a loose screwdriver inside an engine nacelle during a routine post-flight inspection.'},
    {'id': 33, 'type': 'FOD (Foreign Object Debris)', 'severity': 'Low', 'date': '2025-01-18', 'location': 'Security', 'description': 'A plastic packaging strap was found on the ramp near an active aircraft. Removed immediately.'},
    {'id': 34, 'type': 'Near Miss (Air)', 'severity': 'High', 'date': '2025-07-06', 'location': 'Administration', 'description': "TCAS Resolution Advisory (RA) triggered when two aircraft on intersecting routes climbed/descended into each other's altitude."},
    {'id': 35, 'type': 'Near Miss (Ground)', 'severity': 'Medium', 'date': '2025-07-29', 'location': 'Cabin Crew', 'description': 'Catering truck reversed into a stationary baggage cart'},
    {'id': 36, 'type': 'Near Miss (Ground)', 'severity': 'Low', 'date': '2025-08-23', 'location': 'Flight Operations', 'description': 'Pilot taxied slightly over the stop line on the ramp'},
    {'id': 37, 'type': 'Unauthorized Entry', 'severity': 'Low', 'date': '2025-02-03', 'location': 'Flight Operations', 'description': 'An individual without a boarding pass bypassed security at a small terminal. Apprehended before reaching the aircraft.'},
    {'id': 38, 'type': 'Engine Malfunction', 'severity': 'Low', 'date': '2025-03-09', 'location': 'Flight Operations', 'description': 'Engine oil pressure indication fluctuated during climb. Parameters stabilized at cruise; inspection required post-flight.'},
    {'id': 39, 'type': 'Near Miss (Ground)', 'severity': 'Critical', 'date': '2025-07-07', 'location': 'Cabin Crew', 'description': 'During pushback'},
    {'id': 40, 'type': 'Passenger Misconduct', 'severity': 'Medium', 'date': '2025-07-31', 'location': 'Administration', 'description': 'Passenger verbally abused cabin crew over seating arrangements. Passenger was warned and later calmed down.'},
    {'id': 41, 'type': 'Weather Diversion', 'severity': 'Medium', 'date': '2025-05-11', 'location': 'Administration', 'description': 'Winter storm caused multiple diversions. Crew scheduling was overwhelmed with reassigning crews to avoid duty time violations.'},
    {'id': 42, 'type': 'Medical Emergency', 'severity': 'Critical', 'date': '2025-05-12', 'location': 'Flight Operations', 'description': 'Infant onboard experienced a seizure. Emergency descent initiated and paramedics met the flight.'},
    {'id': 43, 'type': 'Fuel Leak', 'severity': 'Critical', 'date': '2025-06-05', 'location': 'Administration', 'description': 'Fuel leak detected from a ruptured line during refueling. Emergency shutdown initiated; spill contained.'},
    {'id': 44, 'type': 'Weather Diversion', 'severity': 'High', 'date': '2025-08-23', 'location': 'Cabin Crew', 'description': 'Severe turbulence and hail encounter necessitated an immediate diversion. Minor injuries reported among passengers.'},
    {'id': 45, 'type': 'Runway Excursion', 'severity': 'Critical', 'date': '2025-03-27', 'location': 'Engineering', 'description': 'Test aircraft during maintenance check overran the runway after a rejected takeoff due to simulated engine failure.'},
    {'id': 46, 'type': 'Bird Strike', 'severity': 'High', 'date': '2025-03-26', 'location': 'Flight Operations', 'description': 'Bird ingestion into engine #1 on takeoff roll. Engine vibrations noted; takeoff aborted at low speed.'},
    {'id': 47, 'type': 'Medical Emergency', 'severity': 'Low', 'date': '2025-01-16', 'location': 'Administration', 'description': 'Passenger experienced anxiety attack. Calmed by cabin crew with breathing techniques.'},
    {'id': 48, 'type': 'Fuel Leak', 'severity': 'Medium', 'date': '2025-03-14', 'location': 'Administration', 'description': 'Slow leak detected from a fuel panel seal during turnaround. Aircraft taken out of service for repair.'},
    {'id': 49, 'type': 'Hydraulic Failure', 'severity': 'Low', 'date': '2025-02-21', 'location': 'Cabin Crew', 'description': 'Slow hydraulic leak traced to a seal in a galley coffee maker. Unit replaced.'},
    {'id': 50, 'type': 'Turbulence Injury', 'severity': 'Low', 'date': '2025-07-22', 'location': 'Cabin Crew', 'description': 'Passenger hit head on overhead bin during light turbulence while standing. Minor bump treated with ice pack.'},
    {'id': 51, 'type': 'Medical Emergency', 'severity': 'Medium', 'date': '2025-01-19', 'location': 'Engineering', 'description': 'Engineer in the workshop suffered an electric shock from a test unit. Treated by onsite medical team.'},
    {'id': 52, 'type': 'Near Miss (Air)', 'severity': 'Medium', 'date': '2025-06-15', 'location': 'Administration', 'description': 'ATC controller error issued conflicting headings to two aircraft. Conflict resolved with TCAS advisory.'},
    {'id': 53, 'type': 'Unauthorized Entry', 'severity': 'High', 'date': '2025-08-14', 'location': 'Cabin Crew', 'description': 'Passenger attempted to enter the flight deck by force during flight. Restrained by crew and offloaded to police.'},
    {'id': 54, 'type': 'Unauthorized Entry', 'severity': 'Low', 'date': '2025-04-15', 'location': 'Ground Handling', 'description': 'Visitor without a security badge was found in a restricted baggage area. Escorted out after verification.'},
    {'id': 55, 'type': 'Runway Excursion', 'severity': 'Low', 'date': '2025-02-21', 'location': 'Engineering', 'description': 'Small training aircraft veered off taxiway onto grass after a tire blowout. No damage.'},
    {'id': 56, 'type': 'Near Miss (Ground)', 'severity': 'Low', 'date': '2025-05-06', 'location': 'Cabin Crew', 'description': 'Two service vehicles passed closely at a high speed intersection on the ramp. Drivers counseled.'},
    {'id': 57, 'type': 'Engine Malfunction', 'severity': 'Medium', 'date': '2025-07-16', 'location': 'Security', 'description': 'Engine surging noticed during climb. Engine parameters stabilized; flight continued. Detailed inspection required.'},
    {'id': 58, 'type': 'Fuel Leak', 'severity': 'Low', 'date': '2025-09-23', 'location': 'Security', 'description': 'Small fuel stain spotted under a wing during pre-flight walkaround. Checked by engineering; deemed acceptable for flight.'},
    {'id': 59, 'type': 'Slip/Trip/Fall', 'severity': 'Low', 'date': '2025-03-28', 'location': 'Flight Operations', 'description': 'Pilot slipped on wet ramp while performing external walkaround. No injury.'},
    {'id': 60, 'type': 'Slip/Trip/Fall', 'severity': 'High', 'date': '2025-07-13', 'location': 'Cabin Crew', 'description': 'Cabin crew member fell during turbulence'},
    {'id': 61, 'type': 'Fuel Leak', 'severity': 'Medium', 'date': '2025-05-08', 'location': 'Administration', 'description': 'Fuel imbalance detected in flight due to a faulty crossfeed valve. Managed per checklist; maintenance required.'},
    {'id': 62, 'type': 'Engine Malfunction', 'severity': 'Low', 'date': '2025-04-08', 'location': 'Security', 'description': 'Engine oil level found low during pre-flight. Topped up; monitoring required.'},
    {'id': 63, 'type': 'Engine Malfunction', 'severity': 'Critical', 'date': '2025-08-23', 'location': 'Cabin Crew', 'description': 'Engine fire warning illuminated during takeoff roll. Takeoff aborted; emergency evacuation initiated.'},
    {'id': 64, 'type': 'Runway Excursion', 'severity': 'Low', 'date': '2025-09-19', 'location': 'Cabin Crew', 'description': 'Aircraft exited onto a high-speed taxiway at an excessive speed'},
    {'id': 65, 'type': 'Bird Strike', 'severity': 'Medium', 'date': '2025-07-22', 'location': 'Engineering', 'description': 'Bird strike on landing gear during approach. Post-flight inspection revealed no critical damage.'},
    {'id': 66, 'type': 'Weather Diversion', 'severity': 'Low', 'date': '2025-01-25', 'location': 'Security', 'description': 'Flight diverted for operational reasons (airport curfew). Passenger accommodation handled smoothly.'},
    {'id': 67, 'type': 'Hydraulic Failure', 'severity': 'Critical', 'date': '2025-04-30', 'location': 'Security', 'description': 'Loss of all hydraulic pressure during a maintenance test flight. Emergency landing performed using manual reversion.'},
    {'id': 68, 'type': 'Turbulence Injury', 'severity': 'Low', 'date': '2025-08-17', 'location': 'Flight Operations', 'description': 'Passenger spilled hot coffee on themselves during light turbulence. Minor burn treated with first aid.'},
    {'id': 69, 'type': 'Weather Diversion', 'severity': 'Low', 'date': '2025-06-17', 'location': 'Security', 'description': 'Thunderstorm activity caused ground stop'},
    {'id': 70, 'type': 'Passenger Misconduct', 'severity': 'Low', 'date': '2025-04-04', 'location': 'Ground Handling', 'description': 'Dispute between passengers over overhead bin space. De-escalated by ground staff before boarding.'},
    {'id': 71, 'type': 'Unauthorized Entry', 'severity': 'Low', 'date': '2025-08-02', 'location': 'Flight Operations', 'description': 'Passenger boarded with an expired boarding pass. Error caught by gate agent during final scan.'},
    {'id': 72, 'type': 'Weather Diversion', 'severity': 'Medium', 'date': '2025-06-21', 'location': 'Ground Handling', 'description': 'Ice on runway required de-icing operations'},
    {'id': 73, 'type': 'Passenger Misconduct', 'severity': 'Medium', 'date': '2025-04-25', 'location': 'Administration', 'description': 'Passenger became intoxicated and disruptive in the gate area. Denied boarding and handed over to security.'},
    {'id': 74, 'type': 'FOD (Foreign Object Debris)', 'severity': 'Critical', 'date': '2025-02-14', 'location': 'Flight Operations', 'description': 'Maintenance found a metal debris (FOD) inside an engine inlet during a routine inspection.'},
    {'id': 75, 'type': 'Medical Emergency', 'severity': 'Critical', 'date': '2025-03-14', 'location': 'Ground Handling', 'description': 'Ramp agent suffered a cardiac arrest on the tarmac. CPR administered and emergency services responded.'},
    {'id': 76, 'type': 'Fuel Leak', 'severity': 'Low', 'date': '2025-02-18', 'location': 'Flight Operations', 'description': 'Minor fuel seepage observed from a drain valve. Checked by engineers and signed off as within limits.'},
    {'id': 77, 'type': 'Bird Strike', 'severity': 'Low', 'date': '2025-06-30', 'location': 'Cabin Crew', 'description': 'Small bird strike on landing'},
    {'id': 78, 'type': 'Runway Excursion', 'severity': 'Low', 'date': '2025-03-22', 'location': 'Ground Handling', 'description': 'Baggage tug slid on icy pavement and left the paved surface. No damage or injury.'},
    {'id': 79, 'type': 'Fuel Leak', 'severity': 'Low', 'date': '2025-08-23', 'location': 'Security', 'description': 'Strong odor of fuel reported in the cabin during boarding. Source traced to a spill during refueling; cabin aired out.'},
    {'id': 80, 'type': 'Bird Strike', 'severity': 'Low', 'date': '2025-08-27', 'location': 'Engineering', 'description': 'Bird nest debris found in an auxiliary power unit (APU) during a scheduled inspection.'},
    {'id': 81, 'type': 'Medical Emergency', 'severity': 'High', 'date': '2025-07-13', 'location': 'Ground Handling', 'description': 'Passenger collapsed in the security screening area. Suspected stroke; immediate medical assistance provided.'},
    {'id': 82, 'type': 'Near Miss (Air)', 'severity': 'Critical', 'date': '2025-07-16', 'location': 'Security', 'description': 'Loss of separation occurred between two arriving aircraft due to ATC miscommunication. RA triggered.'},
    {'id': 83, 'type': 'Cabin Smoke', 'severity': 'Critical', 'date': '2025-02-20', 'location': 'Flight Operations', 'description': 'Smoke detected in the cabin from an overheated entertainment system unit. Emergency declared; landed safely.'},
    {'id': 84, 'type': 'Passenger Misconduct', 'severity': 'High', 'date': '2025-08-29', 'location': 'Security', 'description': 'Passenger attempted to open a cabin door while the aircraft was taxiing. Subdued by crew and security.'},
    {'id': 85, 'type': 'Weather Diversion', 'severity': 'Medium', 'date': '2025-08-24', 'location': 'Administration', 'description': 'Sandstorm at destination required holding and eventual diversion. Passenger logistics were challenging.'},
    {'id': 86, 'type': 'Passenger Misconduct', 'severity': 'High', 'date': '2025-02-02', 'location': 'Ground Handling', 'description': 'Physical altercation between passengers at the gate area prior to boarding. Police intervention required.'},
    {'id': 87, 'type': 'Near Miss (Ground)', 'severity': 'High', 'date': '2025-01-26', 'location': 'Ground Handling', 'description': "A marshaller's signals were misinterpreted"},
    {'id': 88, 'type': 'Turbulence Injury', 'severity': 'Low', 'date': '2025-01-17', 'location': 'Ground Handling', 'description': 'Passenger reported airsickness during a bumpy approach. Attended to by cabin crew.'},
    {'id': 89, 'type': 'Navigation Error', 'severity': 'Critical', 'date': '2025-06-29', 'location': 'Administration', 'description': 'Incorrect weight and balance data loaded'},
    {'id': 90, 'type': 'Near Miss (Air)', 'severity': 'Low', 'date': '2025-04-01', 'location': 'Administration', 'description': 'Two aircraft on parallel runways conducted simultaneous takeoffs. Wake turbulence concern noted.'},
    {'id': 91, 'type': 'Unauthorized Entry', 'severity': 'Critical', 'date': '2025-07-15', 'location': 'Ground Handling', 'description': 'Individual breached the airfield perimeter fence. Apprehended by security near an active runway.'},
    {'id': 92, 'type': 'Unauthorized Entry', 'severity': 'High', 'date': '2025-07-04', 'location': 'Security', 'description': 'Passenger accessed the flight deck by tailgating an authorized crew member during a crew change.'},
    {'id': 93, 'type': 'Slip/Trip/Fall', 'severity': 'Low', 'date': '2025-01-29', 'location': 'Cabin Crew', 'description': 'Passenger tripped over a bag in the aisle during boarding. No injury reported.'},
    {'id': 94, 'type': 'Navigation Error', 'severity': 'High', 'date': '2025-09-14', 'location': 'Flight Operations', 'description': 'Autopilot malfunction caused an uncommanded descent. Flight crew disconnected AP and regained control.'},
    {'id': 95, 'type': 'Engine Malfunction', 'severity': 'Medium', 'date': '2025-05-03', 'location': 'Flight Operations', 'description': 'Engine oil temperature exceeded limits during climb. Power reduced; temperature normalized. Inspection required.'},
    {'id': 96, 'type': 'Navigation Error', 'severity': 'Critical', 'date': '2025-04-20', 'location': 'Cabin Crew', 'description': 'Incorrect destination airport was initially programmed into the FMS by the relief crew. Corrected before top of descent.'},
    {'id': 97, 'type': 'FOD (Foreign Object Debris)', 'severity': 'High', 'date': '2025-06-22', 'location': 'Flight Operations', 'description': 'Post-flight inspection revealed significant damage to a fan blade consistent with FOD ingestion.'},
    {'id': 98, 'type': 'Near Miss (Air)', 'severity': 'Low', 'date': '2025-04-13', 'location': 'Cabin Crew', 'description': 'Aircraft deviated slightly from assigned altitude due to autopilot mode confusion. Corrected after ATC query.'},
    {'id': 99, 'type': 'Near Miss (Ground)', 'severity': 'High', 'date': '2025-03-09', 'location': 'Flight Operations', 'description': 'During night taxiing'},
    {'id': 100, 'type': 'Fuel Leak', 'severity': 'Critical', 'date': '2025-03-16', 'location': 'Cabin Crew', 'description': 'Fuel leak from a cracked fuel line resulted in a significant spill during refueling. Emergency procedures activated.'},

]


class SimpleAIAgent:
    def __init__(self):
        OPENAI.api_key = os.getenv('OPENAI_API_KEY')
        self.df = pd.DataFrame(incidents_data)

    def ask_question(self, question):
        """Super simple AI agent - no SQL, just smart filtering"""
        try:
            # Convert DataFrame to text for AI to understand
            data_context = f"Incident data: {self.df.to_string()}"

            prompt = f"""
            {data_context}

            Question: {question}

            Analyze the incident data and provide a helpful answer. Focus on:
            - Counting incidents by type/severity
            - Finding patterns or trends
            - Identifying high-risk areas

            Answer clearly and include specific numbers from the data.
            """

            response = OPENAI.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            answer = response.choices[0].message.content
            return answer

        except Exception as e:
            return f"I encountered an error: {str(e)}. But here's what I can tell you from the data..."


# Create agent instance
agent = SimpleAIAgent()
