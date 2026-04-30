import React, { useState } from 'react';

const Forge = () => {
  const [mode, setMode] = useState('unit');
  const [unitData, setUnitData] = useState({
    name: 'Warrior',
    max_hp: 10,
    attack: 2,
    defense: 2,
    range: 1,
    traits: ''
  });
  const [tribeData, setTribeData] = useState({
    name: 'The Aethereal',
    home_layer: 1,
    feature: 'Cloud-Sails. All units gain "Flyer" trait at Rank 1 Veterancy.',
    starting_tech: 'Flight'
  });
  const [status, setStatus] = useState('');

  // Prepare payload based on mode
  const currentData = mode === 'unit' ? 
    { 
      ...unitData, 
      traits: unitData.traits.split(',').map(t => t.trim()).filter(t => t) 
    } : 
    tribeData;

  const handleUnitChange = (e) => {
    const { name, value } = e.target;
    setUnitData(prev => ({ 
      ...prev, 
      [name]: (name === 'name' || name === 'traits') ? value : Number(value) 
    }));
  };

  const handleTribeChange = (e) => {
    const { name, value } = e.target;
    setTribeData(prev => ({ 
      ...prev, 
      [name]: name === 'home_layer' ? Number(value) : value 
    }));
  };

  const exportToEngine = async () => {
    setStatus('Exporting...');
    const endpoint = mode === 'unit' ? '/api/units' : '/api/tribes';
    
    try {
      // Assumes FastAPI is running on default port 8000
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentData)
      });
      const result = await response.json();
      
      if (response.ok) {
        setStatus(`✅ Success: ${result.message}`);
      } else {
        setStatus(`❌ Error: ${JSON.stringify(result.detail || result)}`);
      }
    } catch (err) {
      setStatus(`❌ Network Error: Make sure backend is running (localhost:8000)`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-6 md:p-10 font-sans selection:bg-blue-500/30">
      <div className="max-w-6xl mx-auto">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 pb-6 border-b border-gray-800 gap-4">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-500">
              Terra Forge
            </h1>
            <p className="text-gray-400 text-sm mt-2 font-mono">Headless Engine Configurator Pipeline</p>
          </div>
          <div className="flex bg-gray-900 rounded-lg p-1 border border-gray-800 shadow-inner">
            <button 
              className={`px-6 py-2.5 rounded-md font-semibold text-sm transition-all duration-200 ${mode === 'unit' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/50' : 'text-gray-500 hover:text-gray-300'}`}
              onClick={() => { setMode('unit'); setStatus(''); }}
            >
              Unit Mode
            </button>
            <button 
              className={`px-6 py-2.5 rounded-md font-semibold text-sm transition-all duration-200 ${mode === 'tribe' ? 'bg-purple-600 text-white shadow-lg shadow-purple-900/50' : 'text-gray-500 hover:text-gray-300'}`}
              onClick={() => { setMode('tribe'); setStatus(''); }}
            >
              Tribe Mode
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Left Panel - Input Form */}
          <div className="bg-gray-900 p-6 lg:p-8 rounded-2xl border border-gray-800 shadow-2xl relative overflow-hidden">
            {/* Subtle background glow */}
            <div className={`absolute top-0 right-0 w-64 h-64 opacity-10 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none ${mode === 'unit' ? 'bg-blue-500' : 'bg-purple-500'}`}></div>

            <h2 className="text-xl font-bold mb-8 flex items-center text-gray-200">
              <span className={`w-2.5 h-6 rounded-full mr-3 ${mode === 'unit' ? 'bg-blue-500' : 'bg-purple-500'}`}></span>
              Define {mode === 'unit' ? 'Unit Parameters' : 'Tribe Parameters'}
            </h2>
            
            {mode === 'unit' ? (
              <div className="space-y-6 relative z-10">
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Unit Name</label>
                  <input type="text" name="name" value={unitData.name} onChange={handleUnitChange} className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-100 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors outline-none" />
                </div>
                
                <div className="bg-gray-950 p-4 rounded-xl border border-gray-800 space-y-5">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 flex justify-between items-center">
                      <span>Max HP (1-40)</span>
                      <span className="text-blue-400 font-mono bg-blue-900/30 px-2 py-0.5 rounded">{unitData.max_hp}</span>
                    </label>
                    <input type="range" name="max_hp" min="1" max="40" value={unitData.max_hp} onChange={handleUnitChange} className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-blue-500" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 flex justify-between items-center">
                      <span>Attack (1-40)</span>
                      <span className="text-red-400 font-mono bg-red-900/30 px-2 py-0.5 rounded">{unitData.attack}</span>
                    </label>
                    <input type="range" name="attack" min="1" max="40" value={unitData.attack} onChange={handleUnitChange} className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-red-500" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 flex justify-between items-center">
                      <span>Defense (1-40)</span>
                      <span className="text-indigo-400 font-mono bg-indigo-900/30 px-2 py-0.5 rounded">{unitData.defense}</span>
                    </label>
                    <input type="range" name="defense" min="1" max="40" value={unitData.defense} onChange={handleUnitChange} className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-indigo-500" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Range</label>
                    <input type="number" name="range" min="1" value={unitData.range} onChange={handleUnitChange} className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-100 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors outline-none font-mono" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Traits (comma sep)</label>
                    <input type="text" name="traits" value={unitData.traits} onChange={handleUnitChange} placeholder="e.g. Sky-native" className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-100 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors outline-none" />
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-6 relative z-10">
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Tribe Name</label>
                  <input type="text" name="name" value={tribeData.name} onChange={handleTribeChange} className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-100 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors outline-none" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Home Layer (Z-Axis)</label>
                  <select name="home_layer" value={tribeData.home_layer} onChange={handleTribeChange} className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-100 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors outline-none font-mono">
                    <option value="1">1 : Heavens</option>
                    <option value="0">0 : Surface</option>
                    <option value="-1">-1 : Mantle</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Starting Technology</label>
                  <input type="text" name="starting_tech" value={tribeData.starting_tech} onChange={handleTribeChange} className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-100 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors outline-none" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Unique Feature</label>
                  <textarea name="feature" value={tribeData.feature} onChange={handleTribeChange} rows="3" className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-gray-100 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors outline-none resize-none" />
                </div>
              </div>
            )}

            <div className="mt-8 pt-6 border-t border-gray-800 relative z-10">
              <button 
                onClick={exportToEngine}
                className={`w-full py-4 rounded-xl font-bold text-white shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 active:translate-y-0 flex justify-center items-center gap-2 ${mode === 'unit' ? 'bg-blue-600 hover:bg-blue-500 shadow-blue-900/40' : 'bg-purple-600 hover:bg-purple-500 shadow-purple-900/40'}`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
                Export to Engine
              </button>
              
              {/* Status Message */}
              <div className="h-6 mt-4">
                {status && (
                  <p className="text-sm text-center font-mono animate-pulse text-gray-300">
                    {status}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Right Panel - JSON Output Preview */}
          <div className="bg-[#0D1117] p-1 rounded-2xl border border-gray-800 shadow-2xl flex flex-col h-[600px] lg:h-auto">
            <div className="bg-gray-900/50 px-4 py-3 border-b border-gray-800 flex justify-between items-center rounded-t-xl">
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                <span className="text-xs font-mono text-gray-400 uppercase tracking-widest">Compiler Payload Preview</span>
              </div>
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-gray-700"></div>
                <div className="w-3 h-3 rounded-full bg-gray-700"></div>
                <div className="w-3 h-3 rounded-full bg-gray-700"></div>
              </div>
            </div>
            <div className="flex-grow p-6 overflow-auto custom-scrollbar">
              <pre className="text-emerald-400 font-mono text-sm leading-relaxed">
                {JSON.stringify(currentData, null, 2)}
              </pre>
            </div>
          </div>

        </div>
      </div>
      
      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
          height: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #0D1117; 
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #374151; 
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #4B5563; 
        }
      `}} />
    </div>
  );
};

export default Forge;
