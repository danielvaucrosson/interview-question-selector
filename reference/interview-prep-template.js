// ============================================================
// Interview Document Generator — Reference Template
// ============================================================
// This is an anonymized, reusable template for generating
// formatted interview question documents (.docx) using docx-js.
//
// To use: replace placeholder values (marked with {{PLACEHOLDER}})
// with actual candidate/role data, then run with Node.js.
//
// Dependencies: npm install docx
// ============================================================

const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, LevelFormat } = require('docx');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0 };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

const DARK_BLUE = "1F3864";
const MED_BLUE = "2E75B6";
const LIGHT_BLUE = "D6E4F0";
const LIGHT_GRAY = "F2F2F2";

function headerCell(text, width) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: { fill: DARK_BLUE, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: "FFFFFF", font: "Arial", size: 20 })] })]
  });
}

function cell(children, width, opts = {}) {
  return new TableCell({
    borders, width: { size: width, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: cellMargins,
    verticalAlign: "top",
    children: Array.isArray(children) ? children : [children]
  });
}

function questionBlock(q) {
  const diffLabels = { 0: "Intro", 1: "Foundational", 2: "Applied", 3: "Architectural" };
  const diffColors = { 0: "2E75B6", 1: "70AD47", 2: "ED7D31", 3: "C00000" };

  const elements = [];

  // Question ID + metadata row as a compact table
  const metaTable = new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1800, 2500, 2000, 1560, 1500],
    rows: [
      new TableRow({ children: [
        headerCell("ID", 1800),
        headerCell("Domain", 2500),
        headerCell("Technology", 2000),
        headerCell("Difficulty", 1560),
        headerCell("Type", 1500),
      ]}),
      new TableRow({ children: [
        cell(new Paragraph({ children: [new TextRun({ text: q.id, font: "Arial", size: 20, bold: true })] }), 1800),
        cell(new Paragraph({ children: [new TextRun({ text: q.subdomain, font: "Arial", size: 18 })] }), 2500),
        cell(new Paragraph({ children: [new TextRun({ text: q.tech || "General", font: "Arial", size: 18 })] }), 2000),
        cell(new Paragraph({ children: [new TextRun({ text: `${q.diff} - ${diffLabels[q.diff]}`, font: "Arial", size: 18, color: diffColors[q.diff] || "000000", bold: true })] }), 1560),
        cell(new Paragraph({ children: [new TextRun({ text: q.type, font: "Arial", size: 18, italics: true })] }), 1500),
      ]}),
    ]
  });
  elements.push(metaTable);
  elements.push(new Paragraph({ spacing: { before: 120 }, children: [] }));

  // Question text
  elements.push(new Paragraph({
    spacing: { before: 80, after: 80 },
    children: [
      new TextRun({ text: "Q: ", bold: true, font: "Arial", size: 22, color: MED_BLUE }),
      new TextRun({ text: q.question, font: "Arial", size: 22 })
    ]
  }));

  // Answer key header
  elements.push(new Paragraph({
    spacing: { before: 120, after: 40 },
    shading: { type: ShadingType.CLEAR, fill: LIGHT_BLUE },
    children: [new TextRun({ text: "  Ideal Answer Components:", bold: true, font: "Arial", size: 20, color: DARK_BLUE })]
  }));

  // Answer bullets
  const bullets = q.answer.split("\n").filter(b => b.trim());
  for (const bullet of bullets) {
    elements.push(new Paragraph({
      spacing: { before: 40, after: 40 },
      indent: { left: 360 },
      children: [new TextRun({ text: bullet.trim(), font: "Arial", size: 19 })]
    }));
  }

  // Notes box
  elements.push(new Paragraph({
    spacing: { before: 120, after: 40 },
    children: [new TextRun({ text: "Notes:", bold: true, font: "Arial", size: 20 })]
  }));
  const boxBorder = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
  const boxBorders = { top: boxBorder, bottom: boxBorder, left: boxBorder, right: boxBorder };
  elements.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({
      height: { value: 1200, rule: "atLeast" },
      children: [new TableCell({
        borders: boxBorders,
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
      })]
    })]
  }));

  // Rating label + options + input box in a row
  elements.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [7560, 1800],
    rows: [new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          width: { size: 7560, type: WidthType.DXA },
          margins: { top: 60, bottom: 60, left: 0, right: 120 },
          verticalAlign: "center",
          children: [new Paragraph({ children: [
            new TextRun({ text: "Rating:  ", bold: true, font: "Arial", size: 20 }),
            new TextRun({ text: "1 (Weak)  2 (Below)  3 (Meets)  4 (Strong)  5 (Exceptional)", font: "Arial", size: 18 }),
          ]})]
        }),
        new TableCell({
          borders: boxBorders,
          width: { size: 1800, type: WidthType.DXA },
          shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
          margins: { top: 60, bottom: 60, left: 120, right: 120 },
          verticalAlign: "center",
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
        }),
      ]
    })]
  }));
  elements.push(new Paragraph({ spacing: { after: 120 }, children: [] }));

  // Separator
  elements.push(new Paragraph({
    spacing: { after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: MED_BLUE, space: 1 } },
    children: []
  }));

  return elements;
}

// ==================== INTERVIEW METADATA ====================
// Replace these placeholders with actual interview data.

const INTERVIEW = {
  candidateName: "{{CANDIDATE_NAME}}",
  interviewDate: "{{INTERVIEW_DATE}}",
  interviewer: "{{INTERVIEWER_NAME}}",
  jobTitle: "{{JOB_TITLE}}",
  company: "{{COMPANY_NAME}}",
  seniorityLabel: "{{SENIORITY_LEVEL}}",
  questionCount: "{{QUESTION_COUNT}}",
  estimatedDuration: "{{DURATION}}",
  outputPath: "{{OUTPUT_PATH}}",
};

// ==================== QUESTIONS ====================
// Organize questions into sections. Each section has a title,
// subtitle (interviewer guidance), and an array of questions.
//
// Each question needs:
//   id        - question bank ID or custom (e.g., INTRO-001)
//   diff      - 0 (Intro), 1 (Foundational), 2 (Applied), 3 (Architectural)
//   type      - "definition", "explanation", or "scenario"
//   subdomain - sub-domain label from the question bank
//   tech      - technology code(s) or "\u2014" for intro questions
//   question  - verbatim question text
//   answer    - bullet-separated ideal answer components (\n-delimited)

const sections = [
  {
    title: "INTRODUCTION (5 MIN)",
    subtitle: "Let the candidate settle in. Listen for narrative clarity, career arc, and what they emphasize.",
    questions: [
      {
        id: "INTRO-001", diff: 0, type: "scenario",
        subdomain: "Introduction",
        tech: "\u2014",
        question: "Tell me about yourself \u2014 walk me through your background and what brings you here today. (5 minutes)",
        answer: "\u2022 Clear, concise narrative arc connecting past roles to this opportunity\n\u2022 Highlights relevant experience without reading a resume back\n\u2022 Mentions both technical depth and client-facing or consulting work\n\u2022 Signals progression: growing scope, ownership, or complexity over time\n\u2022 Listen for: does their story land in under 5 minutes? Do they self-edit well?"
      },
      {
        id: "INTRO-002", diff: 0, type: "scenario",
        subdomain: "Motivation & Fit",
        tech: "\u2014",
        question: "Why this company, and why this role specifically?",
        answer: "\u2022 Shows they researched the company: what it does, culture, positioning\n\u2022 Articulates why the role appeals vs. other opportunities\n\u2022 Connects their skills to the role\u2019s specific requirements\n\u2022 Genuine enthusiasm or thoughtful reasoning \u2014 not generic answers\n\u2022 Bonus: mentions company values, team culture, or specific projects they found"
      },
    ]
  },
  {
    title: "WARM-UP & ROLE FIT",
    subtitle: "Start conversational. Assess motivation, consulting experience, and communication style.",
    questions: [
      {
        id: "DA-GEN-003", diff: 2, type: "scenario",
        subdomain: "Business Requirements Translation",
        tech: "{{PRIMARY_TECH}}",
        question: "Two business units define a key metric differently. Both insist theirs is the standard. How do you resolve this?",
        answer: "\u2022 Interview each stakeholder to uncover the business decision their definition supports\n\u2022 Propose both as named, documented metrics rather than forcing premature convergence\n\u2022 Facilitate joint session anchored to company-level strategic goals\n\u2022 Implement via governed metric definitions with documentation\n\u2022 Use prioritization framework to determine the executive dashboard default"
      },
    ]
  },
  {
    title: "CORE TECHNICAL SKILLS",
    subtitle: "Primary assessment area. Test depth in the role's key technologies.",
    questions: [
      // {{INSERT_CORE_QUESTIONS_FROM_QUESTION_BANK}}
      // Example:
      // {
      //   id: "DV-PBI-001", diff: 1, type: "definition",
      //   subdomain: "Performance Optimization",
      //   tech: "PBI",
      //   question: "Question text here...",
      //   answer: "\u2022 Bullet 1\n\u2022 Bullet 2\n\u2022 Bullet 3"
      // },
    ]
  },
  {
    title: "ARCHITECTURE & DESIGN",
    subtitle: "Tests system thinking, migration planning, and platform knowledge.",
    questions: [
      // {{INSERT_ARCHITECTURE_QUESTIONS_FROM_QUESTION_BANK}}
    ]
  },
  {
    title: "COMMUNICATION & CLIENT MANAGEMENT",
    subtitle: "Consulting and communication skills. Critical for senior-level roles.",
    questions: [
      // {{INSERT_SOFT_SKILL_QUESTIONS_FROM_QUESTION_BANK}}
    ]
  },
  {
    title: "CLOSING \u2014 DEPTH CHECK",
    subtitle: "One final technical deep-dive to confirm seniority level.",
    questions: [
      // {{INSERT_CLOSING_QUESTION_FROM_QUESTION_BANK}}
    ]
  }
];

// ==================== BUILD DOCUMENT ====================

const allChildren = [];

// Title page
allChildren.push(new Paragraph({ spacing: { before: 3000 }, children: [] }));
allChildren.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: "Interview Question Set", font: "Arial", size: 48, bold: true, color: DARK_BLUE })]
}));
allChildren.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 120 },
  children: [new TextRun({ text: INTERVIEW.jobTitle, font: "Arial", size: 28, color: MED_BLUE })]
}));
allChildren.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 600 },
  children: [new TextRun({ text: `${INTERVIEW.company} \u2014 ${INTERVIEW.seniorityLabel}`, font: "Arial", size: 24, color: "444444" })]
}));

// Candidate info box
const infoTable = new Table({
  width: { size: 6000, type: WidthType.DXA },
  columnWidths: [2400, 3600],
  alignment: AlignmentType.CENTER,
  rows: [
    new TableRow({ children: [
      cell(new Paragraph({ children: [new TextRun({ text: "Candidate:", bold: true, font: "Arial", size: 20 })] }), 2400, { shading: LIGHT_GRAY }),
      cell(new Paragraph({ children: [new TextRun({ text: INTERVIEW.candidateName, font: "Arial", size: 20 })] }), 3600),
    ]}),
    new TableRow({ children: [
      cell(new Paragraph({ children: [new TextRun({ text: "Date:", bold: true, font: "Arial", size: 20 })] }), 2400, { shading: LIGHT_GRAY }),
      cell(new Paragraph({ children: [new TextRun({ text: INTERVIEW.interviewDate, font: "Arial", size: 20 })] }), 3600),
    ]}),
    new TableRow({ children: [
      cell(new Paragraph({ children: [new TextRun({ text: "Interviewer:", bold: true, font: "Arial", size: 20 })] }), 2400, { shading: LIGHT_GRAY }),
      cell(new Paragraph({ children: [new TextRun({ text: INTERVIEW.interviewer, font: "Arial", size: 20 })] }), 3600),
    ]}),
    new TableRow({ children: [
      cell(new Paragraph({ children: [new TextRun({ text: "Questions:", bold: true, font: "Arial", size: 20 })] }), 2400, { shading: LIGHT_GRAY }),
      cell(new Paragraph({ children: [new TextRun({ text: INTERVIEW.questionCount, font: "Arial", size: 20 })] }), 3600),
    ]}),
    new TableRow({ children: [
      cell(new Paragraph({ children: [new TextRun({ text: "Est. Duration:", bold: true, font: "Arial", size: 20 })] }), 2400, { shading: LIGHT_GRAY }),
      cell(new Paragraph({ children: [new TextRun({ text: INTERVIEW.estimatedDuration, font: "Arial", size: 20 })] }), 3600),
    ]}),
  ]
});
allChildren.push(infoTable);

allChildren.push(new Paragraph({ spacing: { before: 600 }, children: [] }));

// Difficulty distribution summary (computed dynamically)
const allQuestions = sections.flatMap(s => s.questions);
const diffCounts = { 0: 0, 1: 0, 2: 0, 3: 0 };
for (const q of allQuestions) { diffCounts[q.diff] = (diffCounts[q.diff] || 0) + 1; }

const distParts = [];
distParts.push(new TextRun({ text: "Difficulty Distribution:  ", font: "Arial", size: 20 }));
if (diffCounts[0]) {
  distParts.push(new TextRun({ text: `${diffCounts[0]} Intro`, font: "Arial", size: 20, bold: true, color: "2E75B6" }));
  distParts.push(new TextRun({ text: "  \u2022  ", font: "Arial", size: 20, color: "CCCCCC" }));
}
if (diffCounts[1]) {
  distParts.push(new TextRun({ text: `${diffCounts[1]} Foundational`, font: "Arial", size: 20, bold: true, color: "70AD47" }));
  distParts.push(new TextRun({ text: "  \u2022  ", font: "Arial", size: 20, color: "CCCCCC" }));
}
if (diffCounts[2]) {
  distParts.push(new TextRun({ text: `${diffCounts[2]} Applied`, font: "Arial", size: 20, bold: true, color: "ED7D31" }));
  distParts.push(new TextRun({ text: "  \u2022  ", font: "Arial", size: 20, color: "CCCCCC" }));
}
if (diffCounts[3]) {
  distParts.push(new TextRun({ text: `${diffCounts[3]} Architectural`, font: "Arial", size: 20, bold: true, color: "C00000" }));
}

allChildren.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 80 },
  children: distParts
}));

// Page break before questions
allChildren.push(new Paragraph({ children: [new PageBreak()] }));

// Sections with questions
for (const section of sections) {
  if (section.questions.length === 0) continue; // skip empty sections

  // Section header
  allChildren.push(new Paragraph({
    spacing: { before: 200, after: 80 },
    shading: { type: ShadingType.CLEAR, fill: DARK_BLUE },
    indent: { left: -120, right: -120 },
    children: [new TextRun({ text: `  ${section.title}`, font: "Arial", size: 24, bold: true, color: "FFFFFF" })]
  }));
  allChildren.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({ text: section.subtitle, font: "Arial", size: 19, italics: true })]
  }));

  for (const q of section.questions) {
    const block = questionBlock(q);
    allChildren.push(...block);
  }
}

// ==================== OVERALL ASSESSMENT PAGE ====================

allChildren.push(new Paragraph({ children: [new PageBreak()] }));
allChildren.push(new Paragraph({
  spacing: { after: 200 },
  shading: { type: ShadingType.CLEAR, fill: DARK_BLUE },
  children: [new TextRun({ text: "  OVERALL ASSESSMENT", font: "Arial", size: 24, bold: true, color: "FFFFFF" })]
}));

const assessBoxBorder = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
const assessBoxBorders = { top: assessBoxBorder, bottom: assessBoxBorder, left: assessBoxBorder, right: assessBoxBorder };

// Configure assessment dimensions for the role
const assessmentRows = [
  "Technical Depth",
  "Data Modeling & Architecture Understanding",
  "Platform & Tooling Experience",
  "Client Communication & Storytelling",
  "Problem-Solving & Consulting Judgment",
  "Pre-Sales / POC Capability"
];
for (const label of assessmentRows) {
  // Label + rating scale + input box row
  allChildren.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [5760, 2000, 1600],
    rows: [new TableRow({
      children: [
        new TableCell({
          borders: { top: assessBoxBorder, bottom: assessBoxBorder, left: assessBoxBorder, right: { style: BorderStyle.NONE, size: 0 } },
          width: { size: 5760, type: WidthType.DXA },
          margins: { top: 60, bottom: 60, left: 120, right: 60 },
          verticalAlign: "center",
          children: [new Paragraph({ children: [new TextRun({ text: label, bold: true, font: "Arial", size: 19 })] })]
        }),
        new TableCell({
          borders: { top: assessBoxBorder, bottom: assessBoxBorder, left: { style: BorderStyle.NONE, size: 0 }, right: { style: BorderStyle.NONE, size: 0 } },
          width: { size: 2000, type: WidthType.DXA },
          margins: { top: 60, bottom: 60, left: 60, right: 60 },
          verticalAlign: "center",
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "1\u20135:", font: "Arial", size: 18 })] })]
        }),
        new TableCell({
          borders: assessBoxBorders,
          width: { size: 1600, type: WidthType.DXA },
          shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
          margins: { top: 60, bottom: 60, left: 120, right: 120 },
          verticalAlign: "center",
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
        }),
      ]
    })]
  }));
  // Notes box
  allChildren.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({
      height: { value: 600, rule: "atLeast" },
      children: [new TableCell({
        borders: assessBoxBorders,
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 18 })] })]
      })]
    })]
  }));
  allChildren.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
}

// Overall recommendation with options + input box
allChildren.push(new Paragraph({ spacing: { before: 300, after: 60 }, children: [
  new TextRun({ text: "Overall Recommendation:", bold: true, font: "Arial", size: 22 }),
]}));
allChildren.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [7200, 2160],
  rows: [new TableRow({
    children: [
      new TableCell({
        borders: noBorders,
        width: { size: 7200, type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 0, right: 120 },
        verticalAlign: "center",
        children: [new Paragraph({ children: [new TextRun({ text: "Strong Hire  /  Hire  /  Maybe  /  No Hire", font: "Arial", size: 20 })] })]
      }),
      new TableCell({
        borders: assessBoxBorders,
        width: { size: 2160, type: WidthType.DXA },
        shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        verticalAlign: "center",
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
      }),
    ]
  })]
}));

// Summary notes box
allChildren.push(new Paragraph({ spacing: { before: 200, after: 60 }, children: [
  new TextRun({ text: "Summary Notes:", bold: true, font: "Arial", size: 20 }),
]}));
allChildren.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [9360],
  rows: [new TableRow({
    height: { value: 2400, rule: "atLeast" },
    children: [new TableCell({
      borders: assessBoxBorders,
      width: { size: 9360, type: WidthType.DXA },
      shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
    })]
  })]
}));

// ==================== ATS EVALUATION FORM ====================
// Configurable post-interview evaluation template.
// Adapt labels and prompts to match your ATS (TeamTailor, Greenhouse, Lever, etc.)

allChildren.push(new Paragraph({ children: [new PageBreak()] }));
allChildren.push(new Paragraph({
  spacing: { after: 80 },
  shading: { type: ShadingType.CLEAR, fill: DARK_BLUE },
  children: [new TextRun({ text: "  ATS EVALUATION \u2014 Technical Interview | General Template", font: "Arial", size: 24, bold: true, color: "FFFFFF" })]
}));
allChildren.push(new Paragraph({
  spacing: { after: 200 },
  children: [new TextRun({ text: "Complete this section after the interview and transfer responses to your ATS.", font: "Arial", size: 19, italics: true })]
}));

const evalBoxBorder = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
const evalBoxBorders = { top: evalBoxBorder, bottom: evalBoxBorder, left: evalBoxBorder, right: evalBoxBorder };

// Helper for evaluation questions with rating
function evalQuestion(label, prompt, hasRating = true) {
  const elems = [];
  elems.push(new Paragraph({
    spacing: { before: 240, after: 60 },
    shading: { type: ShadingType.CLEAR, fill: LIGHT_BLUE },
    children: [new TextRun({ text: `  ${label}`, font: "Arial", size: 21, bold: true, color: DARK_BLUE })]
  }));
  elems.push(new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({ text: prompt, font: "Arial", size: 20 })]
  }));
  if (hasRating) {
    elems.push(new Table({
      width: { size: 9360, type: WidthType.DXA },
      columnWidths: [7560, 1800],
      rows: [new TableRow({
        children: [
          new TableCell({
            borders: noBorders,
            width: { size: 7560, type: WidthType.DXA },
            margins: { top: 60, bottom: 60, left: 0, right: 120 },
            verticalAlign: "center",
            children: [new Paragraph({ children: [
              new TextRun({ text: "Rating (1\u20135):  ", bold: true, font: "Arial", size: 20 }),
              new TextRun({ text: "1 (Weak)  2 (Below)  3 (Meets)  4 (Strong)  5 (Exceptional)", font: "Arial", size: 18 }),
            ]})]
          }),
          new TableCell({
            borders: evalBoxBorders,
            width: { size: 1800, type: WidthType.DXA },
            shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
            margins: { top: 60, bottom: 60, left: 120, right: 120 },
            verticalAlign: "center",
            children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
          }),
        ]
      })]
    }));
  }
  elems.push(new Paragraph({ spacing: { before: 40, after: 40 }, children: [new TextRun({ text: "Notes:", bold: true, font: "Arial", size: 20 })] }));
  elems.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({
      height: { value: 1000, rule: "atLeast" },
      children: [new TableCell({
        borders: evalBoxBorders,
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
      })]
    })]
  }));
  return elems;
}

// Helper for evaluation questions with selectable options
function evalQuestionOptions(label, prompt, options) {
  const elems = [];
  elems.push(new Paragraph({
    spacing: { before: 240, after: 60 },
    shading: { type: ShadingType.CLEAR, fill: LIGHT_BLUE },
    children: [new TextRun({ text: `  ${label}`, font: "Arial", size: 21, bold: true, color: DARK_BLUE })]
  }));
  elems.push(new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({ text: prompt, font: "Arial", size: 20 })]
  }));
  const optText = options.join("  /  ");
  elems.push(new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [7200, 2160],
    rows: [new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          width: { size: 7200, type: WidthType.DXA },
          margins: { top: 60, bottom: 60, left: 0, right: 120 },
          verticalAlign: "center",
          children: [new Paragraph({ children: [new TextRun({ text: optText, font: "Arial", size: 19 })] })]
        }),
        new TableCell({
          borders: evalBoxBorders,
          width: { size: 2160, type: WidthType.DXA },
          shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
          margins: { top: 60, bottom: 60, left: 120, right: 120 },
          verticalAlign: "center",
          children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
        }),
      ]
    })]
  }));
  return elems;
}

// Evaluation dimensions — customize per your ATS template
allChildren.push(...evalQuestion(
  "Tech Skills",
  "What are the main technical strengths you observed in the candidate during the interview?"
));
allChildren.push(...evalQuestion(
  "Consulting Skills",
  "How would you rate the candidate\u2019s consulting skills, particularly in their capacity to comprehend client requirements and deliver impactful solutions? Why?"
));
allChildren.push(...evalQuestion(
  "Seniority",
  "Does the candidate possess the appropriate seniority for the role, in your assessment?"
));
allChildren.push(...evalQuestion(
  "Communication",
  "How would you describe the candidate\u2019s communication style during the interview?"
));
allChildren.push(...evalQuestion(
  "Cultural Fit",
  "In your opinion, does the candidate demonstrate a good cultural fit with the team and the organization? Why?"
));
allChildren.push(...evalQuestion(
  "Weaknesses / Areas for Improvement",
  "Please share your insights into the candidate\u2019s identified weaknesses or areas for improvement.",
  false
));

// ==================== INTERNAL ONLY PAGE ====================

allChildren.push(new Paragraph({ children: [new PageBreak()] }));
allChildren.push(new Paragraph({
  spacing: { after: 200 },
  shading: { type: ShadingType.CLEAR, fill: "C00000" },
  children: [new TextRun({ text: "  INTERNAL ONLY", font: "Arial", size: 24, bold: true, color: "FFFFFF" })]
}));

allChildren.push(...evalQuestionOptions(
  "[Internal] Seniority Classification",
  "Based on the candidate\u2019s experience and responses, how would you classify their seniority level?",
  ["Junior", "Mid", "Semi Senior", "Senior", "Expert/Technical Lead", "Manager/Director"]
));

allChildren.push(...evalQuestionOptions(
  "[Internal] Recommendation",
  "Would you recommend moving this candidate forward to the next step in the hiring process?",
  ["Yes", "No"]
));

allChildren.push(new Paragraph({
  spacing: { before: 240, after: 60 },
  shading: { type: ShadingType.CLEAR, fill: LIGHT_BLUE },
  children: [new TextRun({ text: "  [Internal] Feedback and Comments", font: "Arial", size: 21, bold: true, color: DARK_BLUE })]
}));
allChildren.push(new Paragraph({
  spacing: { after: 80 },
  children: [new TextRun({ text: "Any additional comments or observations from the interview.", font: "Arial", size: 20 })]
}));
allChildren.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [9360],
  rows: [new TableRow({
    height: { value: 2400, rule: "atLeast" },
    children: [new TableCell({
      borders: evalBoxBorders,
      width: { size: 9360, type: WidthType.DXA },
      shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 20 })] })]
    })]
  })]
}));

// ==================== GENERATE DOCUMENT ====================

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: MED_BLUE, space: 4 } },
          children: [
            new TextRun({ text: `${INTERVIEW.company} \u2014 Interview: ${INTERVIEW.candidateName}`, font: "Arial", size: 16, color: "999999" }),
          ]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({ text: "Page ", font: "Arial", size: 16, color: "999999" }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: "999999" }),
          ]
        })]
      })
    },
    children: allChildren
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(INTERVIEW.outputPath, buffer);
  console.log(`Done! File written to ${INTERVIEW.outputPath}`);
});
