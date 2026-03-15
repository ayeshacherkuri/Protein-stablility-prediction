import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, CheckCircle2, FlaskConical, RotateCcw, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/Card';
import { cn } from '../lib/utils';

const Predict = () => {
    const [sequence, setSequence] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const API_URL = 'http://localhost:5000/predict';

    const handlePredict = async (e) => {
        e.preventDefault();
        if (!sequence.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sequence: sequence.trim() }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to predict stability');
            }

            setResult(data);
        } catch (err) {
            setError(err.message || 'An unexpected error occurred');
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setSequence('');
        setResult(null);
        setError(null);
    };

    const sampleSequence = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG";

    return (
        <div className="container py-12 md:py-20 max-w-5xl">
            <div className="flex flex-col items-center text-center mb-10">
                <h1 className="text-3xl md:text-4xl font-bold mb-4">Protein Stability Analysis</h1>
                <p className="text-muted-foreground max-w-2xl">
                    Enter an amino acid sequence below to predict its stability score and classification using our deep learning model.
                </p>
            </div>

            <div className="grid gap-8 md:grid-cols-[1.5fr,1fr]">

                {/* Input Section */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <Card className="h-full">
                        <CardHeader>
                            <CardTitle>Input Sequence</CardTitle>
                            <CardDescription>
                                Paste your amino acid sequence (e.g., standard one-letter codes like 'M', 'K', 'A').
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handlePredict} className="space-y-4">
                                <div className="relative">
                                    <textarea
                                        value={sequence}
                                        onChange={(e) => setSequence(e.target.value.toUpperCase())}
                                        placeholder="Enter sequence here..."
                                        className="flex min-h-[200px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 font-mono"
                                        spellCheck="false"
                                    />
                                    <div className="absolute bottom-2 right-2 text-xs text-muted-foreground">
                                        Len: {sequence.length}
                                    </div>
                                </div>

                                <div className="flex flex-col sm:flex-row gap-2 justify-between">
                                    <div className="text-xs text-muted-foreground self-center">
                                        Don't have one? <button type="button" onClick={() => setSequence(sampleSequence)} className="text-primary underline cursor-pointer hover:no-underline">Try sample</button>
                                    </div>
                                    <div className="flex gap-2">
                                        <Button type="button" variant="outline" onClick={handleReset} disabled={loading || !sequence}>
                                            <RotateCcw className="mr-2 h-4 w-4" /> Reset
                                        </Button>
                                        <Button type="submit" disabled={loading || !sequence} isLoading={loading}>
                                            Run Analysis
                                        </Button>
                                    </div>
                                </div>

                                {error && (
                                    <div className="p-3 rounded-md bg-destructive/10 text-destructive text-sm flex items-center gap-2">
                                        <AlertCircle className="h-4 w-4" />
                                        {error}
                                    </div>
                                )}
                            </form>
                        </CardContent>
                    </Card>
                </motion.div>

                {/* Results Section */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                >
                    <AnimatePresence mode="wait">
                        {!result ? (
                            <Card className="h-full flex items-center justify-center min-h-[300px] bg-muted/30 border-dashed">
                                <div className="text-center p-6">
                                    <FlaskConical className="h-12 w-12 text-muted-foreground/40 mx-auto mb-4" />
                                    <h3 className="text-lg font-medium text-muted-foreground">Ready to Analyze</h3>
                                    <p className="text-sm text-muted-foreground/70 mt-2">
                                        Results will appear here after analysis.
                                    </p>
                                </div>
                            </Card>
                        ) : (
                            <motion.div
                                key="results"
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                className="h-full"
                            >
                                <Card className="h-full border-primary/20 bg-primary/5">
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <CheckCircle2 className="h-5 w-5 text-green-600" />
                                            Analysis Complete
                                        </CardTitle>
                                        <CardDescription>
                                            Confidence: {(result.confidence * 100).toFixed(1)}%
                                        </CardDescription>
                                    </CardHeader>
                                    <CardContent className="space-y-6">

                                        {/* Main Score */}
                                        <div className="text-center p-6 bg-background rounded-lg border shadow-sm">
                                            <div className="text-sm font-medium text-muted-foreground uppercase tracking-wide mb-1">Stability Score</div>
                                            <div className={cn(
                                                "text-4xl font-bold mb-2",
                                                result.classification === 'Stable' ? 'text-green-600' : 'text-red-500'
                                            )}>
                                                {result.stability_score.toFixed(2)}
                                            </div>
                                            <div className={cn(
                                                "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
                                                result.classification === 'Stable'
                                                    ? 'border-transparent bg-green-100 text-green-700 hover:bg-green-200'
                                                    : 'border-transparent bg-red-100 text-red-700 hover:bg-red-200'
                                            )}>
                                                {result.classification}
                                            </div>
                                        </div>

                                        {/* Features Grid */}
                                        <div className="grid grid-cols-3 gap-2 text-center">
                                            <div className="p-2 bg-background rounded border">
                                                <div className="text-xl font-bold">{result.features.hydrophobic_count}</div>
                                                <div className="text-[10px] uppercase text-muted-foreground">Hydrophobic</div>
                                            </div>
                                            <div className="p-2 bg-background rounded border">
                                                <div className="text-xl font-bold">{result.features.charged_count}</div>
                                                <div className="text-[10px] uppercase text-muted-foreground">Charged</div>
                                            </div>
                                            <div className="p-2 bg-background rounded border">
                                                <div className="text-xl font-bold">{result.features.polar_count}</div>
                                                <div className="text-[10px] uppercase text-muted-foreground">Polar</div>
                                            </div>
                                        </div>

                                        <div className="text-sm text-muted-foreground pt-2 border-t text-center">
                                            Sequence length: {result.sequence_length} residues
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.div>
            </div>
        </div>
    );
};

export default Predict;
