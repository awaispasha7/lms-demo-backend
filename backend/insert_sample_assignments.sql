-- Insert Sample Assignments into Supabase
-- Includes: Quizzes, MCQs, Short Answers, True/False, and Homework
-- Run this in Supabase SQL Editor after creating the tables

-- First, clear any existing assignments (optional - remove if you want to keep existing data)
-- DELETE FROM assignments;

-- ============================================
-- QUIZZES (Quick assessments with mixed question types)
-- ============================================

-- Quiz 1: Quick Math Quiz (Mixed: MCQ + True/False)
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Quick Math Quiz',
  'A short quiz covering basic algebra and geometry concepts. Mix of multiple choice and true/false questions.',
  '[
    {
      "questionNumber": 1,
      "questionText": "What is 15 × 8?",
      "options": ["100", "120", "105", "115"],
      "correctOptions": [1],
      "rubric": "Multiply: 15 × 8 = 120",
      "marks": 1,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "The area of a circle is πr²",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "Yes, the formula for the area of a circle is πr² where r is the radius.",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 3,
      "questionText": "What is the square root of 144?",
      "options": ["10", "11", "12", "13"],
      "correctOptions": [2],
      "rubric": "12 × 12 = 144, so √144 = 12",
      "marks": 1,
      "type": "mcq"
    },
    {
      "questionNumber": 4,
      "questionText": "All triangles have three sides",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "By definition, a triangle is a polygon with exactly three sides.",
      "marks": 1,
      "type": "true_false"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '3 days'),
  (NOW() - INTERVAL '1 day')
);

-- Quiz 2: Science Quick Check (True/False focused)
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Science Quick Check',
  'True or False quiz on basic science facts.',
  '[
    {
      "questionNumber": 1,
      "questionText": "Water boils at 100°C at sea level",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "At standard atmospheric pressure (sea level), water boils at 100°C (212°F).",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 2,
      "questionText": "The human body has 206 bones",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "An adult human skeleton typically consists of 206 bones.",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 3,
      "questionText": "Photosynthesis produces oxygen",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "During photosynthesis, plants convert carbon dioxide and water into glucose and oxygen.",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 4,
      "questionText": "The speed of light is faster than the speed of sound",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "Light travels at approximately 299,792,458 m/s, while sound travels at about 343 m/s in air.",
      "marks": 1,
      "type": "true_false"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '2 days'),
  (NOW() - INTERVAL '2 days')
);

-- ============================================
-- MCQ ASSIGNMENTS (Multiple Choice Questions)
-- ============================================

-- MCQ Assignment 1: History Multiple Choice
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'World History - Multiple Choice',
  'Multiple choice questions covering major world history events and figures.',
  '[
    {
      "questionNumber": 1,
      "questionText": "In which year did World War II end?",
      "options": ["1943", "1944", "1945", "1946"],
      "correctOptions": [2],
      "rubric": "World War II ended in 1945 with the surrender of Japan in September.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "Who wrote ''The Communist Manifesto''?",
      "options": ["Vladimir Lenin", "Karl Marx and Friedrich Engels", "Joseph Stalin", "Leon Trotsky"],
      "correctOptions": [1],
      "rubric": "Karl Marx and Friedrich Engels co-authored ''The Communist Manifesto'' in 1848.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 3,
      "questionText": "Which ancient civilization built the pyramids?",
      "options": ["Romans", "Greeks", "Egyptians", "Mayans"],
      "correctOptions": [2],
      "rubric": "The ancient Egyptians built the famous pyramids, most notably the Great Pyramid of Giza.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 4,
      "questionText": "The Renaissance period began in which country?",
      "options": ["France", "Germany", "Italy", "Spain"],
      "correctOptions": [2],
      "rubric": "The Renaissance began in Italy in the 14th century, particularly in cities like Florence and Venice.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 5,
      "questionText": "Which war was fought between 1861-1865?",
      "options": ["World War I", "American Civil War", "Revolutionary War", "War of 1812"],
      "correctOptions": [1],
      "rubric": "The American Civil War was fought from 1861 to 1865 between the Union and the Confederacy.",
      "marks": 2,
      "type": "mcq"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '7 days'),
  (NOW() - INTERVAL '2 days')
);

-- MCQ Assignment 2: Biology Multiple Choice
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Biology - Cell Structure MCQ',
  'Multiple choice questions about cell biology and structure.',
  '[
    {
      "questionNumber": 1,
      "questionText": "Which organelle is known as the ''powerhouse of the cell''?",
      "options": ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"],
      "correctOptions": [1],
      "rubric": "Mitochondria are called the powerhouse because they produce ATP (energy) through cellular respiration.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "What is the function of the cell membrane?",
      "options": ["Protein synthesis", "Control what enters and exits the cell", "DNA storage", "Energy production"],
      "correctOptions": [1],
      "rubric": "The cell membrane is selectively permeable and controls the movement of substances in and out of the cell.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 3,
      "questionText": "Which type of cell lacks a nucleus?",
      "options": ["Eukaryotic", "Prokaryotic", "Plant cell", "Animal cell"],
      "correctOptions": [1],
      "rubric": "Prokaryotic cells (like bacteria) do not have a membrane-bound nucleus, while eukaryotic cells do.",
      "marks": 2,
      "type": "mcq"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '5 days'),
  (NOW() - INTERVAL '1 day')
);

-- ============================================
-- SHORT ANSWER ASSIGNMENTS
-- ============================================

-- Short Answer Assignment 1: Literature Analysis
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Literature - Short Answer Analysis',
  'Short answer questions requiring brief written responses about literary themes and characters.',
  '[
    {
      "questionNumber": 1,
      "questionText": "In 2-3 sentences, explain the main theme of ''Romeo and Juliet''.",
      "options": ["Short answer - type your response"],
      "correctOptions": [0],
      "rubric": "Look for answers mentioning themes like: forbidden love, fate vs. free will, the consequences of feuding families, or the power of love to overcome obstacles. Key themes include the destructive nature of hatred and the transformative power of love.",
      "marks": 5,
      "type": "short_answer"
    },
    {
      "questionNumber": 2,
      "questionText": "Describe the character development of the protagonist in ''To Kill a Mockingbird''. (3-4 sentences)",
      "options": ["Short answer - type your response"],
      "correctOptions": [0],
      "rubric": "Answers should discuss Scout''s growth from innocence to understanding, her learning about prejudice and justice, and how her perspective changes through the events of the novel.",
      "marks": 6,
      "type": "short_answer"
    },
    {
      "questionNumber": 3,
      "questionText": "What is the significance of the green light in ''The Great Gatsby''? (2-3 sentences)",
      "options": ["Short answer - type your response"],
      "correctOptions": [0],
      "rubric": "The green light represents Gatsby''s hopes and dreams, particularly his desire to be with Daisy. It symbolizes the American Dream and the unattainable nature of his aspirations.",
      "marks": 5,
      "type": "short_answer"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '10 days'),
  (NOW() - INTERVAL '3 days')
);

-- Short Answer Assignment 2: Science Explanations
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Chemistry - Short Answer Explanations',
  'Explain chemical processes and concepts in your own words.',
  '[
    {
      "questionNumber": 1,
      "questionText": "Explain the difference between an element and a compound. (2-3 sentences)",
      "options": ["Short answer - type your response"],
      "correctOptions": [0],
      "rubric": "An element is a pure substance made of only one type of atom (e.g., gold, oxygen). A compound is a substance made of two or more different elements chemically bonded together (e.g., water H₂O, salt NaCl).",
      "marks": 4,
      "type": "short_answer"
    },
    {
      "questionNumber": 2,
      "questionText": "Describe what happens during a chemical reaction. (3-4 sentences)",
      "options": ["Short answer - type your response"],
      "correctOptions": [0],
      "rubric": "During a chemical reaction, bonds between atoms are broken and new bonds are formed. Reactants are transformed into products with different properties. Energy may be absorbed or released. The total mass is conserved.",
      "marks": 5,
      "type": "short_answer"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '8 days'),
  (NOW() - INTERVAL '2 days')
);

-- ============================================
-- TRUE/FALSE ASSIGNMENTS
-- ============================================

-- True/False Assignment 1: Geography Facts
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Geography - True or False',
  'True or False questions about world geography and landmarks.',
  '[
    {
      "questionNumber": 1,
      "questionText": "Mount Everest is the tallest mountain in the world",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "Mount Everest, at 8,848.86 meters (29,031.7 ft), is the highest point on Earth above sea level.",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 2,
      "questionText": "The Amazon River is the longest river in the world",
      "options": ["True", "False"],
      "correctOptions": [1],
      "rubric": "The Nile River is the longest river in the world (about 6,650 km). The Amazon is the second longest but has the largest volume of water.",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 3,
      "questionText": "Australia is both a country and a continent",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "Australia is unique in being both a country and a continent. It is the smallest continent and the sixth-largest country.",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 4,
      "questionText": "The Sahara Desert is the largest desert in the world",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "The Sahara Desert is the largest hot desert in the world, covering approximately 9.2 million square kilometers.",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 5,
      "questionText": "Russia spans across two continents",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "Russia spans across both Europe and Asia, making it a transcontinental country.",
      "marks": 1,
      "type": "true_false"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '4 days'),
  (NOW() - INTERVAL '1 day')
);

-- ============================================
-- HOMEWORK ASSIGNMENTS (Comprehensive, mixed types)
-- ============================================

-- Homework 1: Calculus I - Derivatives and Applications (Original, now marked as homework)
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Calculus I - Derivatives and Applications (Homework)',
  'This homework assignment covers fundamental concepts of derivatives, including the power rule, chain rule, and applications to optimization problems.',
  '[
    {
      "questionNumber": 1,
      "questionText": "What is the derivative of f(x) = x³ + 5x² - 3x + 7?",
      "options": ["3x² + 10x - 3", "x² + 5x - 3", "3x² + 5x - 3", "x³ + 10x - 3"],
      "correctOptions": [0],
      "rubric": "Apply the power rule: d/dx(xⁿ) = nxⁿ⁻¹. For each term, multiply the coefficient by the exponent and reduce the exponent by 1.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "If f(x) = (x² + 1)⁵, which rule should you use to find the derivative?",
      "options": ["Power Rule", "Chain Rule", "Product Rule", "Quotient Rule"],
      "correctOptions": [1],
      "rubric": "The Chain Rule is used when you have a function inside another function. Here, (x² + 1) is inside the power function.",
      "marks": 1,
      "type": "mcq"
    },
    {
      "questionNumber": 3,
      "questionText": "A rectangular box with a square base has a volume of 64 cm³. What is the minimum surface area?",
      "options": ["64 cm²", "96 cm²", "128 cm²", "192 cm²"],
      "correctOptions": [1],
      "rubric": "Set up the optimization problem: V = x²h = 64, so h = 64/x². Surface area S = 2x² + 4xh. Substitute h and find the derivative to minimize.",
      "marks": 3,
      "type": "mcq"
    },
    {
      "questionNumber": 4,
      "questionText": "What is the derivative of sin(x) with respect to x?",
      "options": ["cos(x)", "-cos(x)", "sin(x)", "-sin(x)"],
      "correctOptions": [0],
      "rubric": "The derivative of sin(x) is cos(x). This is a fundamental trigonometric derivative that should be memorized.",
      "marks": 1,
      "type": "mcq"
    },
    {
      "questionNumber": 5,
      "questionText": "If a function has a local maximum at x = a, what can you say about f''(a)?",
      "options": ["f''(a) > 0", "f''(a) < 0", "f''(a) = 0", "f''(a) is undefined"],
      "correctOptions": [2],
      "rubric": "At a local maximum, the derivative is zero (horizontal tangent). This is a critical point where the function changes from increasing to decreasing.",
      "marks": 2,
      "type": "mcq"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '7 days'),
  (NOW() - INTERVAL '2 days')
);

-- Homework 2: Physics I - Newtonian Mechanics (Original, now marked as homework)
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Physics I - Newtonian Mechanics (Homework)',
  'This homework assignment covers Newton''s laws of motion, forces, and energy conservation principles.',
  '[
    {
      "questionNumber": 1,
      "questionText": "According to Newton''s First Law, an object at rest will:",
      "options": ["Accelerate if a force is applied", "Remain at rest unless acted upon by a net external force", "Move with constant velocity", "Always experience friction"],
      "correctOptions": [1],
      "rubric": "Newton''s First Law states that an object at rest stays at rest, and an object in motion stays in motion with constant velocity, unless acted upon by a net external force.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "A 10 kg block is pushed with a force of 50 N. If the coefficient of friction is 0.3, what is the acceleration? (g = 10 m/s²)",
      "options": ["2 m/s²", "5 m/s²", "8 m/s²", "10 m/s²"],
      "correctOptions": [0],
      "rubric": "Calculate: F_net = F_applied - F_friction = 50 - (0.3 × 10 × 10) = 50 - 30 = 20 N. Then a = F_net/m = 20/10 = 2 m/s².",
      "marks": 3,
      "type": "mcq"
    },
    {
      "questionNumber": 3,
      "questionText": "Which of the following is a conservative force?",
      "options": ["Friction", "Air resistance", "Gravitational force", "Normal force"],
      "correctOptions": [2],
      "rubric": "Conservative forces are path-independent and allow for potential energy. Gravity, electric forces, and spring forces are conservative. Friction and air resistance are non-conservative.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 4,
      "questionText": "A ball is thrown upward with initial velocity 20 m/s. What is its velocity at the maximum height?",
      "options": ["20 m/s upward", "0 m/s", "20 m/s downward", "10 m/s upward"],
      "correctOptions": [1],
      "rubric": "At the maximum height, the vertical velocity is zero. The ball momentarily stops before falling back down due to gravity.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 5,
      "questionText": "In a perfectly elastic collision, which quantity is conserved?",
      "options": ["Only momentum", "Only kinetic energy", "Both momentum and kinetic energy", "Neither momentum nor kinetic energy"],
      "correctOptions": [2],
      "rubric": "In a perfectly elastic collision, both momentum and kinetic energy are conserved. This is different from inelastic collisions where only momentum is conserved.",
      "marks": 2,
      "type": "mcq"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '5 days'),
  (NOW() - INTERVAL '1 day')
);

-- Homework 3: Mixed Type Homework (MCQ + Short Answer + True/False)
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Comprehensive Science Homework',
  'A comprehensive homework assignment with multiple question types covering various science topics.',
  '[
    {
      "questionNumber": 1,
      "questionText": "Which planet is closest to the Sun?",
      "options": ["Venus", "Mercury", "Earth", "Mars"],
      "correctOptions": [1],
      "rubric": "Mercury is the closest planet to the Sun in our solar system.",
      "marks": 1,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "The human heart has four chambers",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "The human heart has four chambers: two atria (upper) and two ventricles (lower).",
      "marks": 1,
      "type": "true_false"
    },
    {
      "questionNumber": 3,
      "questionText": "Explain the water cycle in 3-4 sentences.",
      "options": ["Short answer - type your response"],
      "correctOptions": [0],
      "rubric": "Answers should mention: evaporation (water turns to vapor), condensation (vapor forms clouds), precipitation (rain/snow), and collection (water returns to bodies of water). The cycle is continuous.",
      "marks": 5,
      "type": "short_answer"
    },
    {
      "questionNumber": 4,
      "questionText": "What is the chemical formula for water?",
      "options": ["H₂O", "CO₂", "O₂", "NaCl"],
      "correctOptions": [0],
      "rubric": "Water is composed of two hydrogen atoms and one oxygen atom, giving it the chemical formula H₂O.",
      "marks": 1,
      "type": "mcq"
    },
    {
      "questionNumber": 5,
      "questionText": "Photosynthesis only occurs during the day",
      "options": ["True", "False"],
      "correctOptions": [0],
      "rubric": "Photosynthesis requires light energy, which is only available during daylight hours. At night, plants perform cellular respiration instead.",
      "marks": 1,
      "type": "true_false"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '6 days'),
  (NOW() - INTERVAL '4 days')
);

-- Homework 4: Linear Algebra - Matrix Operations (Original, now marked as homework)
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Linear Algebra - Matrix Operations (Homework)',
  'This homework assignment covers matrix multiplication, determinants, and solving systems of linear equations.',
  '[
    {
      "questionNumber": 1,
      "questionText": "What is the determinant of a 2×2 matrix [[a, b], [c, d]]?",
      "options": ["ad + bc", "ad - bc", "ab - cd", "a + d - b - c"],
      "correctOptions": [1],
      "rubric": "For a 2×2 matrix, the determinant is calculated as ad - bc. This is the product of the main diagonal minus the product of the off-diagonal.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "For matrix multiplication A × B to be defined, what must be true?",
      "options": ["A and B must have the same dimensions", "The number of columns in A must equal the number of rows in B", "The number of rows in A must equal the number of columns in B", "A and B must be square matrices"],
      "correctOptions": [1],
      "rubric": "Matrix multiplication requires that the number of columns in the first matrix equals the number of rows in the second matrix. The resulting matrix has dimensions (rows of A) × (columns of B).",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 3,
      "questionText": "A system of linear equations has no solution when:",
      "options": ["The determinant is zero", "The system is consistent", "The equations are linearly dependent", "The system is inconsistent"],
      "correctOptions": [3],
      "rubric": "An inconsistent system has no solution, meaning the equations contradict each other. This can be identified when row reduction leads to a contradiction like 0 = 1.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 4,
      "questionText": "What is the inverse of a matrix A?",
      "options": ["A matrix B such that A + B = I", "A matrix B such that A × B = B × A = I", "A matrix B such that A - B = 0", "The transpose of A"],
      "correctOptions": [1],
      "rubric": "The inverse of matrix A, denoted A⁻¹, is the matrix such that A × A⁻¹ = A⁻¹ × A = I, where I is the identity matrix. Not all matrices have inverses.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 5,
      "questionText": "What does it mean if the determinant of a matrix is zero?",
      "options": ["The matrix is invertible", "The matrix is singular (not invertible)", "All entries are zero", "The matrix is symmetric"],
      "correctOptions": [1],
      "rubric": "A matrix with zero determinant is called singular and does not have an inverse. This occurs when the rows (or columns) are linearly dependent.",
      "marks": 2,
      "type": "mcq"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '10 days'),
  (NOW() - INTERVAL '3 days')
);

-- Homework 5: Physics II - Electric Fields and Potential (Original, now marked as homework)
INSERT INTO assignments (title, description, questions, due_date, created_at)
VALUES (
  'Physics II - Electric Fields and Potential (Homework)',
  'This homework assignment covers electric fields, electric potential, and Gauss''s law applications.',
  '[
    {
      "questionNumber": 1,
      "questionText": "What is the direction of the electric field around a positive point charge?",
      "options": ["Radially inward", "Radially outward", "Tangential to the charge", "No direction (zero field)"],
      "correctOptions": [1],
      "rubric": "The electric field around a positive point charge points radially outward, away from the charge. For a negative charge, it points radially inward.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 2,
      "questionText": "Two point charges of +5 μC and -3 μC are separated by 2 meters. What is the magnitude of the force between them? (k = 9 × 10⁹ N⋅m²/C²)",
      "options": ["33.75 N", "67.5 N", "135 N", "270 N"],
      "correctOptions": [0],
      "rubric": "Use Coulomb''s law: F = k|q₁q₂|/r² = (9×10⁹)(5×10⁻⁶)(3×10⁻⁶)/(2²) = 135×10⁻³/4 = 33.75 N. The force is attractive since charges are opposite.",
      "marks": 3,
      "type": "mcq"
    },
    {
      "questionNumber": 3,
      "questionText": "Electric potential is a:",
      "options": ["Vector quantity", "Scalar quantity", "Tensor quantity", "Dimensionless quantity"],
      "correctOptions": [1],
      "rubric": "Electric potential is a scalar quantity, meaning it has magnitude but no direction. This is different from electric field, which is a vector.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 4,
      "questionText": "According to Gauss''s law, the electric flux through a closed surface depends on:",
      "options": ["The shape of the surface", "The size of the surface", "The charge enclosed by the surface", "The electric field outside the surface"],
      "correctOptions": [2],
      "rubric": "Gauss''s law states that the electric flux through a closed surface is proportional to the charge enclosed, regardless of the surface shape or size.",
      "marks": 2,
      "type": "mcq"
    },
    {
      "questionNumber": 5,
      "questionText": "What happens to the electric potential energy when two like charges are brought closer together?",
      "options": ["It increases", "It decreases", "It remains constant", "It becomes zero"],
      "correctOptions": [0],
      "rubric": "For like charges, bringing them closer together increases the potential energy because work must be done against the repulsive force. The system stores more energy.",
      "marks": 2,
      "type": "mcq"
    }
  ]'::jsonb,
  (NOW() + INTERVAL '6 days'),
  (NOW() - INTERVAL '4 days')
);

-- Verify the inserts
SELECT id, title, created_at, due_date FROM assignments ORDER BY created_at;
