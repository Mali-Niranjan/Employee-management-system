
import os

def fix_user_controller_v2():
    path = r'c:\Users\skulk\Desktop\EMS_2.0\emsbackend\controllers\userController.js'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # We need to replace the entire getCompanyStructure function because it was broken
    # First, find the start of the function
    start_index = -1
    for i, line in enumerate(lines):
        if 'export const getCompanyStructure' in line:
            start_index = i
            break
            
    if start_index != -1:
        # Define the corrected function
        new_fn = [
            'export const getCompanyStructure = async (req, res) => {\n',
            '  try {\n',
            '    // Align with Team model: use team_leader instead of steward\n',
            '    // Also populate members.employee to show the full hierarchy\n',
            '    const teams = await Team.find()\n',
            '      .populate("team_leader", "name designation profileImage employeeId")\n',
            '      .populate("members.employee", "name designation profileImage employeeId role");\n',
            '    \n',
            '    // Format the response for the frontend hierarchy\n',
            '    const structure = teams.map(team => ({\n',
            '      _id: team._id,\n',
            '      name: team.team_name, // Map team_name to name\n',
            '      type: "team",\n',
            '      leader: team.team_leader ? {\n',
            '        _id: team.team_leader._id,\n',
            '        name: team.team_leader.name,\n',
            '        designation: team.team_leader.designation,\n',
            '        profileImage: team.team_leader.profileImage,\n',
            '        employeeId: team.team_leader.employeeId\n',
            '      } : null,\n',
            '      children: (team.members || []).map(m => m.employee ? ({\n',
            '        _id: m.employee._id,\n',
            '        name: m.employee.name,\n',
            '        type: "user",\n',
            '        designation: m.employee.designation,\n',
            '        role: m.employee.role,\n',
            '        profileImage: m.employee.profileImage\n',
            '      }) : null).filter(Boolean)\n',
            '    }));\n',
            '\n',
            '    res.status(200).json(structure);\n',
            '  } catch (error) {\n',
            '    console.error("Error fetching company structure:", error);\n',
            '    res.status(500).json({ message: "Server error while fetching company structure" });\n',
            '  }\n',
            '};\n'
        ]
        
        # Replace from start_index to the end of the file (or the next closing brace if it were a multi-export file)
        # Since I added it at the end previously, replacing until end is safe
        final_content = lines[:start_index] + new_fn
    else:
        # If not found, just append (should not happen if I already added it)
        new_fn_str = """
export const getCompanyStructure = async (req, res) => {
  try {
    const teams = await Team.find()
      .populate("team_leader", "name designation profileImage employeeId")
      .populate("members.employee", "name designation profileImage employeeId role");
    
    const structure = teams.map(team => ({
      _id: team._id,
      name: team.team_name,
      type: "team",
      leader: team.team_leader ? {
        _id: team.team_leader._id,
        name: team.team_leader.name,
        designation: team.team_leader.designation,
        profileImage: team.team_leader.profileImage,
        employeeId: team.team_leader.employeeId
      } : null,
      children: (team.members || []).map(m => m.employee ? ({
        _id: m.employee._id,
        name: m.employee.name,
        type: "user",
        designation: m.employee.designation,
        role: m.employee.role,
        profileImage: m.employee.profileImage
      }) : null).filter(Boolean)
    }));

    res.status(200).json(structure);
  } catch (error) {
    console.error("Error fetching company structure:", error);
    res.status(500).json({ message: "Server error while fetching company structure" });
  }
};
"""
        with open(path, 'a', encoding='utf-8') as f:
            f.write(new_fn_str)
        print("Appended corrected getCompanyStructure")
        return

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(final_content)
    print("Fixed userController.js v2")

if __name__ == "__main__":
    fix_user_controller_v2()
