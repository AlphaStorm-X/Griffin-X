import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';

const Analyzer = () => {
  const [image, setImage] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setImage(url);
      setResult(null);
    }
  };

  const simulateScan = () => {
    if (!image) return;
    setIsScanning(true);
    setResult(null);

    // Simulate AI scanning delay
    setTimeout(() => {
      setIsScanning(false);
      setResult({
        name: 'Paracetamol 500mg',
        dosage: '1 tablet every 6-8 hours',
        warning: 'Do not exceed 4000mg in 24 hours. Avoid alcohol.',
        isSafe: true,
      });
    }, 3000);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">Medicine Analyzer</h1>
        <p className="text-slate-500 mt-2">Upload a photo of your pill or prescription to get instant AI-powered details.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="glass-card p-6 flex flex-col items-center justify-center min-h-[400px]">
          {!image ? (
            <div 
              className="w-full h-full border-2 border-dashed border-primary-200 rounded-xl flex flex-col items-center justify-center bg-primary-50/50 hover:bg-primary-50 transition-colors cursor-pointer group"
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="w-16 h-16 rounded-full bg-white flex items-center justify-center text-primary-500 shadow-sm group-hover:scale-110 transition-transform mb-4">
                <UploadCloud size={32} />
              </div>
              <h3 className="font-semibold text-slate-700">Click or drag to upload</h3>
              <p className="text-sm text-slate-500 mt-1">SVG, PNG, JPG or GIF (max. 5MB)</p>
            </div>
          ) : (
            <div className="w-full space-y-4">
              <div className="relative rounded-xl overflow-hidden shadow-sm aspect-[4/3] group">
                <img src={image} alt="Uploaded medicine" className="w-full h-full object-cover" />
                {isScanning && (
                  <>
                    <div className="absolute inset-0 bg-primary-600/20 backdrop-blur-[2px]"></div>
                    <div className="absolute top-0 left-0 w-full h-[2px] bg-primary-400 shadow-[0_0_8px_2px_rgba(56,189,248,0.8)] animate-scan"></div>
                  </>
                )}
                <button 
                  onClick={() => setImage(null)}
                  className="absolute top-2 right-2 p-2 bg-white/80 backdrop-blur rounded-lg text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                  disabled={isScanning}
                >
                  Clear
                </button>
              </div>

              {!result && (
                <button
                  onClick={simulateScan}
                  disabled={isScanning}
                  className="w-full py-3 bg-gradient-to-r from-primary-500 to-blue-500 hover:from-primary-600 hover:to-blue-600 text-white rounded-xl font-medium shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {isScanning ? (
                    <>
                      <Loader2 size={20} className="animate-spin" />
                      Analyzing with AI...
                    </>
                  ) : (
                    <>
                      <ImageIcon size={20} />
                      Analyze Medicine
                    </>
                  )}
                </button>
              )}
            </div>
          )}
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleImageUpload} 
            accept="image/*" 
            className="hidden" 
          />
        </div>

        {/* Results Section */}
        <div className="glass-card p-6 min-h-[400px]">
          <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
            Analysis Results
          </h2>
          
          {isScanning ? (
            <div className="space-y-4">
              <div className="h-6 bg-slate-200 rounded animate-pulse w-3/4"></div>
              <div className="h-4 bg-slate-200 rounded animate-pulse w-1/2"></div>
              <div className="h-20 bg-slate-200 rounded animate-pulse mt-8"></div>
              <div className="h-12 bg-slate-200 rounded animate-pulse"></div>
            </div>
          ) : result ? (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="p-4 bg-green-50 rounded-xl border border-green-100 flex items-start gap-4">
                <CheckCircle2 className="text-green-500 mt-1 shrink-0" size={24} />
                <div>
                  <h3 className="font-bold text-green-900 text-lg">Safe to Consume</h3>
                  <p className="text-green-700 text-sm mt-1">Based on common records, this medicine matches the visual profile.</p>
                </div>
              </div>

              <div>
                <p className="text-sm text-slate-500 uppercase tracking-wider font-semibold mb-1">Identified Medicine</p>
                <p className="text-2xl font-bold text-slate-800">{result.name}</p>
              </div>

              <div>
                <p className="text-sm text-slate-500 uppercase tracking-wider font-semibold mb-1">Recommended Dosage</p>
                <p className="text-lg text-slate-700">{result.dosage}</p>
              </div>

              <div className="p-4 bg-orange-50 rounded-xl border border-orange-100 mt-8">
                <div className="flex items-center gap-2 text-orange-800 font-semibold mb-2">
                  <AlertCircle size={18} /> Safety Warning
                </div>
                <p className="text-sm text-orange-700">{result.warning}</p>
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 space-y-4">
              <Sparkles className="w-12 h-12 opacity-50" />
              <p>Upload an image and run analysis to view detailed medicine insights.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Add this to index.css or a global style block for the scanner line animation
// @keyframes scan {
//   0% { top: 0; }
//   50% { top: 100%; }
//   100% { top: 0; }
// }
// .animate-scan { animation: scan 3s ease-in-out infinite; }

import { Sparkles } from 'lucide-react';
export default Analyzer;
