import React from 'react';
import { Zap, ShieldCheck, Activity, Code, Database, Globe } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '../components/ui/Card';

const features = [
    {
        icon: <Zap className="h-6 w-6 text-yellow-500" />,
        title: "Real-time Prediction",
        description: "Get stability scores in milliseconds using our optimized inference engine."
    },
    {
        icon: <ShieldCheck className="h-6 w-6 text-green-500" />,
        title: "High Accuracy",
        description: "Our CNN model achieves state-of-the-art accuracy on benchmark datasets."
    },
    {
        icon: <Activity className="h-6 w-6 text-blue-500" />,
        title: "Detailed Analytics",
        description: "Breakdown of hydrophobic, charged, and polar residue contributions."
    },
    {
        icon: <Code className="h-6 w-6 text-purple-500" />,
        title: "REST API",
        description: "Integrate our prediction engine into your own workflows via our JSON API."
    },
    {
        icon: <Database className="h-6 w-6 text-red-500" />,
        title: "Extensive Database",
        description: "Trained on thousands of curated protein sequences for robust generalization."
    },
    {
        icon: <Globe className="h-6 w-6 text-cyan-500" />,
        title: "Web Accessible",
        description: "No software to install. Access the tool from any device with a browser."
    }
];

const Features = () => {
    return (
        <div className="container py-12 md:py-20">
            <div className="text-center mb-16">
                <h1 className="text-4xl font-bold mb-4">Key Features</h1>
                <p className="text-muted-foreground max-w-2xl mx-auto">
                    Built for speed, accuracy, and ease of use.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {features.map((feature, index) => (
                    <Card key={index} className="border hover:border-primary/50 transition-colors">
                        <CardHeader>
                            <div className="mb-2 w-fit rounded-lg bg-secondary p-2">
                                {feature.icon}
                            </div>
                            <CardTitle>{feature.title}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <CardDescription className="text-base">
                                {feature.description}
                            </CardDescription>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
};

export default Features;
