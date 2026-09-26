from __future__ import annotations

from typing import Any, Dict


class DemoAIClient:
    def generate_discovery(self, idea: str, audience: str | None, industry: str | None, problem: str | None) -> Dict[str, Any]:
        primary = audience or "founders and early-stage teams"
        secondary = "students, creators, and community builders" if "student" in idea.lower() else "adjacent operators and collaborators"
        return {
            "problem_statement": (problem or "The idea has traction but lacks clear positioning and a differentiated story.") + " The market needs a sharper articulation of the user problem, value, and audience fit.",
            "primary_audience": primary,
            "secondary_audience": secondary,
            "user_pain_points": [
                "Decision-making feels fragmented and slow.",
                "The value proposition is not yet clear enough to excite early users.",
                "Potential customers do not immediately understand why the solution matters."
            ],
            "user_needs": [
                "A compelling narrative that explains the problem clearly.",
                "A brand language consistent across product, website, and outreach.",
                "A sharper target audience and differentiated value proposition."
            ],
            "opportunity": f"{idea.strip()} can stand out by turning a rough opportunity into a focused strategic narrative that feels credible and memorable.",
            "assumptions": [
                "The user has a real pain point worth solving.",
                "The offer becomes much more compelling when the audience is narrowed.",
                "Clarity will improve trust and conversion."
            ],
            "important_questions": [
                "Who feels the pain most urgently and repeatedly?",
                "What makes this solution different from generic alternatives?",
                "What should users remember after hearing the concept once?"
            ],
            "source_facts": {
                "idea": idea,
                "audience": audience,
                "industry": industry,
                "problem": problem,
            }
        }

    def generate_positioning(self, project: Dict[str, Any]) -> Dict[str, Any]:
        discovery = project.get("discovery", {}) or {}
        idea = project.get("idea", "")
        audience = discovery.get("primary_audience") or "target users"
        category = "team discovery platform" if "hackathon" in idea.lower() else "idea-to-brand platform"
        return {
            "category": category,
            "value_proposition": f"A focused system that helps {audience} turn uncertainty into clear strategy, brand direction, and story.",
            "differentiation": "It blends strategic clarity with structured workflow guidance so the brand story is stronger than a collection of one-off AI outputs.",
            "positioning_statement": f"For {audience}, {idea} provides a guided path from rough concept to compelling brand identity, helping teams move from confusion to confident market positioning.",
            "competitive_alternatives": [
                "Generic AI brainstorming tools",
                "Freelance design and naming services",
                "Disconnected brand templates and copy generators"
            ],
            "strategic_opportunity": "Build a premium strategic workspace that keeps the entire brand narrative coherent across discovery, identity, and launch messaging.",
            "potential_positioning_risks": [
                "The idea may feel too broad if the audience is not narrowed quickly.",
                "The value proposition risks sounding like a generic productivity tool.",
                "Without an emotional anchor, the offer may feel design-heavy but strategically weak."
            ],
            "facts_vs_hypotheses": {
                "user_provided_facts": {
                    "idea": idea,
                    "audience": audience,
                    "industry": project.get("industry")
                },
                "ai_generated_hypotheses": [
                    "The market values strategic coherence as much as creative output.",
                    "Users benefit more from structured decision-making than from isolated creative prompts."
                ],
                "assumptions": [
                    "The user wants a premium brand process rather than one-off creative generation."
                ]
            }
        }

    def generate_brand_definition(self, project: Dict[str, Any]) -> Dict[str, Any]:
        position = project.get("positioning", {}) or {}
        audience = (project.get("discovery", {}) or {}).get("primary_audience") or "ambitious builders"
        return {
            "mission": f"Help {audience} move from rough ideas into confident, coherent brands that feel strategically aligned and commercially credible.",
            "brand_principles": [
                "Clarity over noise",
                "Strategic thinking before surface polish",
                "Momentum through focused execution"
            ],
            "personality_traits": [
                {"trait": "Confident", "relevance": "The brand should sound decisive and credible rather than tentative."},
                {"trait": "Human", "relevance": "Messaging should feel grounded, not robotic or inflated."},
                {"trait": "Practical", "relevance": "The brand should speak to real decisions and useful outcomes."},
                {"trait": "Fast", "relevance": "The process feels efficient without sacrificing strategic depth."}
            ],
            "emotional_qualities": ["Trustworthy", "Focused", "Inspiring", "Calm"],
            "voice_characteristics": [
                "Direct and confident",
                "Clear without sounding corporate",
                "Insightful, practical, and concise"
            ],
            "audience_relationship": "The brand should feel like a thoughtful strategic partner that helps people refine ideas into something they can believably launch.",
            "messaging_pillars": [
                "Turn rough ideas into strategic clarity.",
                "Build a distinct brand story that customers understand quickly.",
                "Create brand systems that stay consistent from positioning to launch."
            ],
            "positioning_anchor": position.get("value_proposition")
        }

    def generate_expression(self, project: Dict[str, Any]) -> Dict[str, Any]:
        idea = project.get("idea", "")
        base = idea.split(" ")[:4]
        name_seed = " ".join(base).title()
        return {
            "naming_directions": [
                {
                    "name": f"{name_seed} Labs",
                    "naming_territory": "structured product and strategic brand building",
                    "rationale": "It feels credible, premium, and operational without sounding generic.",
                    "strengths": ["Memorable", "Professional", "Easy to extend"],
                    "risks": ["Can feel broad if the offer is not clearly defined"]
                },
                {
                    "name": f"{name_seed} Studio",
                    "naming_territory": "creative and strategic identity design",
                    "rationale": "It suggests refinement, intent, and craft while remaining approachable.",
                    "strengths": ["Human", "Polished", "Brand-centric"],
                    "risks": ["May feel too design-heavy for product-led positioning"]
                },
                {
                    "name": f"{name_seed} Forge",
                    "naming_territory": "idea-to-brand transformation and momentum",
                    "rationale": "The metaphor signals shaping raw potential into a clear market identity.",
                    "strengths": ["Distinctive", "Action-oriented", "Strong story"],
                    "risks": ["Can skew industrial or hardware if not balanced"]
                }
            ],
            "tagline_options": [
                "Shape a stronger story.",
                "From rough idea to clear brand.",
                "Turn signal into identity.",
                "Build the brand behind the next big move."
            ],
            "messaging": {
                "one_line_description": "A brand strategy workspace that turns rough ideas into clear positioning, compelling narratives, and consistent launch-ready identity.",
                "elevator_pitch": "BrandForge helps early teams and founders turn uncertain ideas into something people instantly understand, remember, and trust.",
                "website_headline": "From a raw idea to a brand people remember.",
                "supporting_statement": "We blend strategic thinking, guided decision-making, and premium brand direction into a single workflow that keeps the story coherent from first insight to launch.",
                "cta": "Start building your brand",
                "short_social_launch_copy": "Turning rough ideas into stronger brands, clearer positioning, and sharper stories."
            },
            "visual_direction": {
                "visual_personality": "Premium, editorial, confident, and restrained.",
                "color_direction": ["soft ivory", "ink black", "muted slate", "deep accent blue"],
                "typography_direction": "High-contrast sans-serif for headings with generous editorial spacing and clear hierarchy.",
                "imagery_direction": "Minimal product scenes, strategic process visuals, and polished concept mockups rather than generic AI imagery.",
                "ui_design_characteristics": ["Calm, minimal layout", "Clear data hierarchy", "Subtle borders and whitespace", "Focused CTA design"]
            }
        }

    def generate_challenge(self, project: Dict[str, Any]) -> Dict[str, Any]:
        discovery = project.get("discovery", {}) or {}
        brand = project.get("brand_definition", {}) or {}
        expression = project.get("expression", {}) or {}
        return {
            "audience_fit": "Strong",
            "positioning_clarity": "Needs refinement",
            "differentiation": "Strong",
            "consistency": "Moderate",
            "contradictions": [
                "The product may feel more like a creative toolkit than a strategic systems platform unless the process is framed as a guided decision engine."
            ],
            "generic_language": [
                "Turn ideas into growth",
                "Build your brand with AI",
                "Powerful brand solutions"
            ],
            "key_issue": f"The brand must clearly distinguish between {discovery.get('primary_audience', 'its audience')} value and generic strategy output. The story is promising, but it should feel more specific and less broad.",
            "recommended_changes": [
                "Narrow the offer around one core transformation: from idea to strategic clarity.",
                "Use a sharper, more exact promise tied to the user’s real pain and timeline.",
                "Align the naming and visual direction with the stronger strategic positioning rather than broad creative language."
            ],
            "brand_insights": {
                "mission_match": brand.get("mission"),
                "voice_alignment": "The tone should remain calm and decisive, not overly clever or overly abstract.",
                "tagline_check": expression.get("tagline_options", ["From rough idea to clear brand."])[0]
            }
        }

    def generate_final_brand_system(self, project: Dict[str, Any]) -> Dict[str, Any]:
        expression = project.get("expression", {}) or {}
        name = expression.get("naming_directions", [{}])[2].get("name", "BrandForge")
        tagline = expression.get("tagline_options", ["From rough idea to clear brand."])[1]
        brand_definition = project.get("brand_definition", {}) or {}
        challenge = project.get("challenge", {}) or {}

        return {
            "brand_name": name,
            "tagline": tagline,
            "problem": "Founders and early teams struggle to turn raw ideas into a coherent, credible brand without strategic clarity.",
            "target_audience": (project.get("discovery", {}) or {}).get("primary_audience") or "ambitious builders",
            "positioning": "A strategic brand workspace for turning rough ideas into clear, differentiated identity and launch-ready story.",
            "value_proposition": "Helps users move from uncertainty to confidence with a structured workflow that keeps strategy, identity, and messaging aligned.",
            "mission": brand_definition.get("mission"),
            "brand_personality": [
                "Confident",
                "Human",
                "Fast",
                "Collaborative",
                "Practical"
            ],
            "messaging_pillars": brand_definition.get("messaging_pillars", []),
            "voice_and_tone": "Clear, thoughtful, and direct. Confident without sounding inflated; practical without feeling generic.",
            "website_headline": expression.get("messaging", {}).get("website_headline", "From a raw idea to a brand people remember."),
            "elevator_pitch": expression.get("messaging", {}).get("elevator_pitch", "A strategic brand system for turning rough ideas into clear identity."),
            "visual_direction": expression.get("visual_direction", {}),
            "brand_stress_test": challenge,
            "final_recommendations": [
                "Keep the narrative anchored to the user’s actual transformation from idea to clarity.",
                "Let the product feel like a premium strategy workspace rather than a generic design utility.",
                "Use the visual system to reinforce calm confidence and strategic rigor."
            ]
        }

    def generate_launch_plan(self, project: Dict[str, Any]) -> Dict[str, Any]:
        final_brand_system = project.get("final_brand_system", {}) or {}
        discovery = project.get("discovery", {}) or {}
        expression = project.get("expression", {}) or {}
        audience = discovery.get("primary_audience") or "early adopters"
        brand_name = final_brand_system.get("brand_name", "BrandForge")
        return {
            "launch_summary": f"Position {brand_name} as a premium strategic workspace that helps {audience} move from rough ideas to launch-ready clarity.",
            "launch_goal": "Make the value proposition immediately understandable and turn the brand system into a concrete go-to-market story.",
            "launch_channels": [
                "Product landing page",
                "Founder-led social launch",
                "Email announcement to early adopters",
                "Community and partner outreach"
            ],
            "launch_checklist": [
                "Publish the landing page with the finalized headline and tagline.",
                "Package the brand story into a short launch deck or announcement post.",
                "Align onboarding copy with the core transformation promise.",
                "Share the launch with the first audience segment and collect feedback."
            ],
            "launch_messaging": {
                "headline": expression.get("messaging", {}).get("website_headline", "From a raw idea to a brand people remember."),
                "primary_pitch": expression.get("messaging", {}).get("elevator_pitch", "A strategic brand system for turning rough ideas into clear identity."),
                "cta": expression.get("messaging", {}).get("cta", "Start building your brand")
            },
            "success_metrics": [
                "Qualified sign-ups from the intended audience",
                "Positive feedback on clarity of the brand promise",
                "Landing page engagement and CTA click-through rate"
            ],
            "launch_timeline": [
                "Day 1: finalize launch copy and page assets",
                "Day 2: publish the launch materials",
                "Day 3: collect initial feedback and refine the message"
            ]
        }
