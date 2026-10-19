
import os

def fix_user_controller():
    path = r'c:\Users\skulk\Desktop\EMS_2.0\emsbackend\controllers\userController.js'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'getCompanyStructure' not in content:
        # Simple append at the end
        new_fn = """

// ---------------- GET COMPANY STRUCTURE ----------------
export const getCompanyStructure = async (req, res) => {
  try {
    const teams = await Team.find().populate("steward", "name designation profileImage employeeId");
    const structure = teams.map(team => ({
      _id: team._id,
      name: team.name,
      description: team.description,
      steward: team.steward ? {
        _id: team.steward._id,
        name: team.steward.name,
        designation: team.steward.designation,
        profileImage: team.steward.profileImage,
        employeeId: team.steward.employeeId
      } : null,
      membersCount: team.members?.length || 0
    }));

    res.status(200).json(structure);
  } catch (error) {
    console.error("Error fetching company structure:", error);
    res.status(500).json({ message: "Server error while fetching company structure" });
  }
};
"""
        with open(path, 'a', encoding='utf-8') as f:
            f.write(new_fn)
        print("Fixed userController.js")

def fix_admin_verify():
    path = r'c:\Users\skulk\Desktop\EMS_2.0\emsfrontend\src\components\AdminDocumentsVerify.jsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Identify the section to replace
    old_section = """          {loading ? (
             <div className="py-32 flex flex-col items-center justify-center">
                <div className="w-12 h-12 rounded-full border-4 border-slate-100 border-t-blue-600 animate-spin" />
                <p className="mt-4 text-slate-400 text-[10px] font-black uppercase tracking-widest">Scanning Document Store...</p>
             </div>
          ) : filtered.length === 0 ? (
             <div className="py-24 flex flex-col items-center justify-center text-center px-6">
                <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-6">
                   <FiCheck className="text-blue-600 text-3xl" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-1">Compliance Cleared</h3>
                <p className="text-xs text-slate-500">No pending verification requests found in the system queue.</p>
             </div>
          ) : ("""

    new_section = """          {loading ? (
             <div className="py-32 flex flex-col items-center justify-center">
                <div className="w-12 h-12 rounded-full border-4 border-slate-100 border-t-blue-600 animate-spin" />
                <p className="mt-4 text-slate-400 text-[10px] font-black uppercase tracking-widest">Scanning Document Store...</p>
             </div>
          ) : error ? (
             <div className="py-20">
                <EmptyState 
                  type="error" 
                  title="Compliance Stream Error" 
                  message="Unable to intercept the document queue. Security audit synchronization failure."
                  onRetry={fetchKycList}
                />
             </div>
          ) : filtered.length === 0 ? (
             <div className="py-20">
                <EmptyState 
                  type={search ? "search" : "empty"}
                  title={search ? "No Tactical Matches" : "Compliance Cleared"}
                  message={search ? `No personnel records match "${search}" in the active audit queue.` : "No pending verification requests found in the system queue."}
                />
             </div>
          ) : ("""

    # Try to find exactly or with normalized spacing
    if old_section in content:
        content = content.replace(old_section, new_section)
    else:
        # Fallback: try to replace based on the unique landmarks
        import re
        pattern = re.escape('{loading ? (') + r".*?" + re.escape(') : (')
        # This is risky, let's just use string replace on parts
        content = content.replace('filtered.length === 0 ? (', 'error ? (\n             <div className="py-20">\n                <EmptyState \n                  type="error" \n                  title="Compliance Stream Error" \n                  message="Unable to intercept the document queue. Security audit synchronization failure."\n                  onRetry={fetchKycList}\n                />\n             </div>\n          ) : filtered.length === 0 ? (')
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed AdminDocumentsVerify.jsx")

if __name__ == "__main__":
    fix_user_controller()
    fix_admin_verify()
