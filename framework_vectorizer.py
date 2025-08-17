from sentence_transformers import SentenceTransformer
import json
from supabase import create_client, Client
import numpy as np

# Configuration
SUPABASE_URL = "https://zogvnojgmeteutpperfg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpvZ3Zub2pnbWV0ZXV0cHBlcmZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyNjgxNzYsImV4cCI6MjA3MDg0NDE3Nn0.-86bWVQDPMp1m1ENAaHCYTnPxIE6eoDhy5aK7EBVXQs"

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
model = SentenceTransformer('all-MiniLM-L6-v2')  # Free, fast, good quality

def get_embedding(text):
    """Generate embedding for text using Hugging Face"""
    embedding = model.encode(text)
    return embedding.tolist()  # Convert numpy array to list for JSON

# All framework chunks from your document
chunks = [
    {
        "chunk_id": "framework_philosophy_001",
        "category": "Core Framework",
        "educational_level": "Universal",
        "content_type": "Foundational Principles",
        "content": """The SHE IS AI educational framework represents a revolutionary approach to artificial intelligence education that prioritizes equity, inclusion, and bias elimination while delivering comprehensive AI literacy across all educational levels. The framework's foundational philosophy centers on the belief that AI education must be accessible to everyone, regardless of background, learning style, or prior technical experience.

The framework operates on seven core principles that guide every aspect of implementation. First, the principle of Universal Accessibility ensures that all learning materials, activities, and assessments are designed to accommodate diverse learning needs, cultural backgrounds, and accessibility requirements. This principle mandates that every component of the framework includes multiple modalities, clear language options, and culturally responsive content that reflects the global nature of AI development and application.

Second, the principle of Bias Elimination requires active identification and mitigation of bias in all educational content, examples, and assessment methods. This goes beyond simply avoiding obviously problematic content to proactively seeking diverse perspectives, challenging assumptions, and creating learning environments where all participants feel valued and represented. The framework includes specific protocols for content review, diverse example selection, and inclusive language use.

Third, the principle of Career Relevance ensures that all learning activities connect directly to real-world AI applications and career opportunities. This principle recognizes that effective AI education must prepare learners for immediate employment or career advancement while building foundational knowledge for lifelong learning in a rapidly evolving field.

Fourth, the principle of Community Building emphasizes the collaborative nature of AI development and the importance of creating supportive learning communities. The framework includes specific strategies for peer learning, mentorship, and professional networking that extend beyond the classroom to create lasting professional relationships and support systems.

Fifth, the principle of Authentic Assessment requires that all evaluation methods create genuine value for learners while accurately measuring their competencies. This principle moves beyond traditional testing to portfolio-based assessment, project work, and real-world application that directly contributes to learners' professional development and career advancement.

Sixth, the principle of Continuous Improvement mandates regular evaluation and refinement of all framework components based on learner outcomes, industry feedback, and emerging best practices in AI education. This principle ensures that the framework remains current, effective, and responsive to changing needs and opportunities.

Seventh, the principle of Ethical Foundation requires that all AI education explicitly addresses ethical considerations, responsible AI development, and the social implications of artificial intelligence. This principle ensures that learners develop not only technical competencies but also the ethical reasoning skills necessary for responsible AI development and deployment.

These principles work together to create an educational experience that is both rigorous and inclusive, preparing learners for successful careers in AI while contributing to a more equitable and representative AI industry. The framework's implementation requires careful attention to these principles at every level, from individual lesson planning to institutional policy development."""
    },
    {
        "chunk_id": "lesson_structure_opening_001",
        "category": "Lesson Structure",
        "educational_level": "Universal",
        "content_type": "Implementation Guide",
        "content": """The Opening Ritual serves as the foundational component of every SHE IS AI framework lesson, creating a consistent, welcoming, and purposeful beginning that sets the tone for inclusive learning and community building. This component typically occupies the first 5-10 minutes of each session and serves multiple critical functions in establishing an effective learning environment.

The Opening Ritual begins with a Community Check-In that acknowledges each learner as a valued member of the learning community. This check-in varies by educational level but always includes an opportunity for learners to share their current state, any challenges they're facing, and their hopes or goals for the session. For elementary learners, this might involve a simple sharing circle where students can express how they're feeling using emotion cards or brief verbal sharing. For professional learners, this might include sharing current AI-related challenges they're facing in their work or recent AI developments they've encountered.

Following the Community Check-In, the Opening Ritual includes a Bias Awareness Moment that explicitly acknowledges the potential for bias in AI systems and in our own thinking. This component helps learners develop the habit of questioning assumptions and considering multiple perspectives. The format varies by educational level, but always includes a brief reflection or discussion about how bias might appear in the day's topic. For younger learners, this might involve examining how different people might have different experiences with technology. For advanced learners, this might include discussion of specific bias examples in AI systems relevant to the day's content.

The third element of the Opening Ritual is the Learning Intention Setting, where learners explicitly articulate what they hope to learn or accomplish during the session. This goes beyond simply reviewing learning objectives to include personal goal setting and connection to individual career or academic aspirations. Learners are encouraged to share how the day's learning connects to their broader goals and to identify specific outcomes they hope to achieve.

The fourth component is the Community Agreement Reinforcement, where the group briefly reviews or reaffirms their shared commitments to inclusive, respectful, and collaborative learning. These agreements are co-created by the learning community and typically include commitments to active listening, respectful disagreement, inclusive language, and mutual support. The specific agreements vary by group but always emphasize the values of equity, inclusion, and collaborative learning.

The Opening Ritual concludes with a Mindfulness or Centering Practice that helps learners transition from external concerns to focused learning. This practice varies by educational level and cultural context but always includes a brief moment of intentional focus and preparation for learning. For some groups, this might involve breathing exercises or brief meditation. For others, it might include visualization of successful learning or affirmation of personal capabilities and goals.

The Opening Ritual is designed to be culturally responsive and adaptable to different learning contexts while maintaining its core functions of community building, bias awareness, intention setting, and learning preparation. Facilitators are encouraged to work with their learning communities to develop Opening Ritual variations that reflect the group's cultural backgrounds, learning preferences, and specific needs while maintaining the component's essential elements and purposes.

Effective implementation of the Opening Ritual requires facilitator preparation, including advance planning of check-in questions, bias awareness topics, and centering practices. Facilitators should also be prepared to adapt the ritual based on group needs, current events, or emerging learning community dynamics while maintaining consistency and predictability that supports learner comfort and engagement."""
    },
    {
        "chunk_id": "lesson_structure_objectives_001",
        "category": "Lesson Structure",
        "educational_level": "Universal",
        "content_type": "Implementation Guide",
        "content": """The Learning Objectives component of the SHE IS AI framework lesson structure serves as the roadmap for each learning session, providing clear, measurable, and meaningful goals that connect to both immediate learning needs and long-term career aspirations. This component typically follows the Opening Ritual and occupies 5-10 minutes of the lesson, establishing clear expectations and success criteria for all participants.

Learning objectives in the SHE IS AI framework are structured using a modified version of Bloom's Taxonomy that specifically incorporates AI literacy competencies and bias awareness skills. Each objective includes three essential elements: the cognitive skill being developed, the AI content or concept being addressed, and the real-world application or career connection. This structure ensures that learners understand not only what they will learn but also why it matters and how it connects to their professional development.

The framework requires that learning objectives be presented in multiple formats to accommodate different learning styles and accessibility needs. Objectives are always presented both verbally and visually, with written versions available in multiple languages when appropriate. Visual representations might include infographics, concept maps, or simple diagrams that illustrate the relationships between different learning goals and their connections to broader AI competencies.

Each learning objective explicitly addresses bias awareness and inclusion considerations. This means that objectives don't simply focus on technical AI concepts but also include goals related to recognizing bias, understanding diverse perspectives, and developing inclusive approaches to AI development and application. For example, a lesson on machine learning algorithms might include objectives related to understanding algorithmic bias, recognizing the importance of diverse training data, and developing strategies for inclusive AI system design.

Learning objectives are always connected to authentic assessment and portfolio development. Learners understand from the beginning of each session how their learning will be demonstrated and how it will contribute to their professional portfolio. This connection helps learners see the immediate value of their learning and motivates engagement with challenging concepts and skills.

The framework emphasizes collaborative objective setting, where learners have opportunities to contribute to or modify learning objectives based on their individual needs, interests, and career goals. This collaborative approach ensures that learning remains relevant and engaging while maintaining the framework's core competency requirements. Facilitators are trained to balance individual learner needs with group learning goals and framework standards.

Learning objectives in the SHE IS AI framework are always presented with success criteria that help learners understand what successful achievement looks like. These criteria are specific, measurable, and include both individual and collaborative elements. Success criteria address not only technical competency but also collaboration skills, bias awareness, and ethical reasoning abilities.

The component includes explicit connections to previous learning and preview of future learning, helping learners understand how each session fits into their broader AI education journey. These connections are particularly important for maintaining motivation and helping learners see the cumulative nature of AI literacy development.

Facilitators are required to check for understanding of learning objectives before proceeding to core content, ensuring that all learners have clarity about expectations and success criteria. This check might involve brief discussions, quick polls, or individual reflection activities that help learners internalize the goals and begin thinking about how they will demonstrate their learning.

The Learning Objectives component concludes with learners setting personal learning intentions that connect the session's objectives to their individual goals and interests. This personal connection helps maintain engagement and motivation throughout the session while ensuring that learning remains relevant to each participant's unique needs and aspirations."""
    },
    {
        "chunk_id": "core_concepts_context_001",
        "category": "Core Content",
        "educational_level": "Universal",
        "content_type": "Conceptual Framework",
        "content": """The "AI in Context" component of the SHE IS AI framework provides learners with essential understanding of artificial intelligence as a sociotechnical phenomenon that exists within complex social, economic, and cultural systems. This foundational concept ensures that learners develop sophisticated understanding of AI that goes beyond technical specifications to encompass the human and societal dimensions of artificial intelligence development and deployment.

AI in Context begins with historical perspective that traces the development of artificial intelligence from its theoretical origins to contemporary applications. This historical view emphasizes the contributions of diverse individuals and communities to AI development, explicitly highlighting the work of women, people of color, and international contributors who are often overlooked in traditional AI narratives. Learners explore how different cultural contexts have shaped AI development priorities and approaches, developing appreciation for the global and multicultural nature of AI innovation.

The framework emphasizes understanding AI as embedded within existing social and economic systems rather than as neutral technology that operates independently of human values and biases. Learners examine how AI systems reflect and potentially amplify existing inequalities, while also exploring how AI can be designed and deployed to promote equity and inclusion. This analysis includes examination of specific case studies that illustrate both problematic and exemplary approaches to AI development and deployment.

Economic context receives significant attention, with learners exploring how AI development is funded, how AI companies operate, and how AI deployment affects different economic sectors and communities. This economic analysis includes attention to labor impacts, with honest discussion of how AI affects different types of work and workers. The framework emphasizes understanding these impacts as policy choices rather than inevitable technological outcomes, empowering learners to envision and work toward more equitable AI futures.

Social context exploration includes examination of how AI systems interact with existing social structures, institutions, and relationships. Learners analyze how AI affects privacy, autonomy, and human agency, while also exploring how AI can support human flourishing and community development. This analysis includes attention to different cultural values and priorities, helping learners understand that there are multiple valid approaches to AI development and governance.

The framework includes significant attention to regulatory and governance contexts, helping learners understand current and emerging approaches to AI oversight and accountability. This includes examination of different national and international approaches to AI governance, with analysis of how different regulatory frameworks reflect different values and priorities. Learners develop understanding of their own roles and responsibilities as AI developers, users, and citizens in shaping AI governance and accountability.

Environmental context receives explicit attention, with learners exploring the environmental impacts of AI development and deployment. This includes understanding the energy requirements of AI systems, the environmental costs of data centers and computing infrastructure, and the potential for AI to support environmental sustainability. Learners develop appreciation for the need to consider environmental impacts in AI decision-making and design.

The AI in Context component emphasizes critical thinking skills that enable learners to analyze new AI developments and applications within their broader contexts. Learners develop frameworks for asking important questions about AI systems, including questions about who benefits, who bears risks, how decisions are made, and what alternatives might exist. These critical thinking skills are essential for responsible AI development and deployment throughout learners' careers.

Practical application of contextual understanding includes exercises where learners analyze current AI news and developments using contextual frameworks. These exercises help learners develop habits of contextual thinking that will serve them throughout their careers in AI-related fields. Learners practice identifying stakeholders, analyzing impacts, and considering alternative approaches to AI development and deployment.

The component concludes with learners developing personal frameworks for contextual AI analysis that they can apply in their professional work. These frameworks reflect the learners' own values, career goals, and cultural contexts while incorporating the analytical tools and perspectives developed through the SHE IS AI framework. This personalization ensures that contextual understanding becomes integrated into learners' professional practice rather than remaining abstract knowledge."""
    },
    {
        "chunk_id": "core_concepts_ethics_001",
        "category": "Core Content",
        "educational_level": "Universal",
        "content_type": "Ethical Framework",
        "content": """Ethics and Responsible AI represents one of the most critical components of the SHE IS AI framework, providing learners with comprehensive understanding of ethical considerations in AI development and deployment. This component goes beyond abstract philosophical discussion to provide practical frameworks, tools, and strategies for ethical decision-making throughout AI careers and applications.

The ethical framework begins with exploration of foundational ethical principles as they apply to artificial intelligence. Learners examine principles of beneficence (doing good), non-maleficence (avoiding harm), autonomy (respecting human agency), and justice (fair distribution of benefits and risks) as they relate to AI systems. These principles are explored through concrete examples and case studies that illustrate how ethical considerations arise in real AI development and deployment scenarios.

Justice receives particular emphasis, with detailed exploration of distributive justice (who gets access to AI benefits), procedural justice (how AI decisions are made), and recognition justice (whose voices and perspectives are included in AI development). Learners examine how different approaches to justice lead to different AI design choices and deployment strategies, developing appreciation for the value-laden nature of AI development decisions.

The framework includes comprehensive exploration of AI bias and fairness, moving beyond simple bias identification to sophisticated understanding of different types of bias, their sources, and strategies for mitigation. Learners explore statistical bias, historical bias, representation bias, and evaluation bias, developing understanding of how these different types of bias interact and compound. The exploration includes hands-on activities where learners identify bias in existing AI systems and develop strategies for bias mitigation.

Privacy and surveillance receive significant attention, with learners exploring how AI systems collect, process, and use personal data. This exploration includes understanding of different privacy frameworks, from individual consent models to collective privacy approaches that consider community and societal impacts. Learners develop practical skills for privacy impact assessment and privacy-preserving AI design.

Transparency and explainability are explored as both technical challenges and ethical requirements. Learners examine different approaches to AI explainability, from technical interpretability methods to communication strategies that make AI decisions understandable to affected individuals and communities. The framework emphasizes that transparency requirements vary based on context and stakeholder needs, requiring thoughtful analysis rather than one-size-fits-all solutions.

Accountability and responsibility frameworks receive detailed attention, with learners exploring how responsibility for AI outcomes can be distributed among developers, deployers, users, and governance institutions. This exploration includes examination of different accountability mechanisms, from technical auditing approaches to legal and regulatory frameworks. Learners develop understanding of their own professional responsibilities and how these responsibilities change based on their roles and contexts.

The framework includes significant attention to global and cultural perspectives on AI ethics, recognizing that ethical frameworks vary across cultures and contexts. Learners explore different cultural approaches to privacy, autonomy, community, and technology, developing appreciation for the need to consider diverse ethical perspectives in AI development. This exploration includes examination of indigenous data sovereignty, different cultural approaches to consent and privacy, and varying perspectives on individual versus collective rights.

Practical application of ethical frameworks includes extensive case study analysis where learners apply ethical reasoning to complex AI scenarios. These case studies are drawn from real-world situations and include scenarios relevant to learners' career goals and interests. Learners practice identifying ethical issues, analyzing stakeholder impacts, and developing ethical solutions that balance competing values and interests.

The component includes development of personal ethical frameworks that learners can apply in their professional work. These frameworks incorporate the ethical principles and analytical tools developed through the SHE IS AI framework while reflecting learners' own values, cultural backgrounds, and career contexts. Learners develop practical tools for ethical decision-making, including checklists, decision trees, and consultation processes.

Professional ethics receive explicit attention, with exploration of professional codes of ethics, professional responsibilities, and strategies for ethical advocacy within organizations and professional communities. Learners develop understanding of how to raise ethical concerns, how to advocate for ethical AI practices, and how to build organizational cultures that support ethical AI development.

The Ethics and Responsible AI component concludes with learners developing action plans for ethical AI practice in their specific career contexts. These action plans include specific commitments, accountability mechanisms, and strategies for continued ethical development throughout their careers. This practical application ensures that ethical understanding translates into ethical action in learners' professional lives."""
    },
    {
        "chunk_id": "assessment_portfolio_001",
        "category": "Assessment",
        "educational_level": "Universal",
        "content_type": "Assessment Strategy",
        "content": """The Portfolio Development component of the SHE IS AI framework represents a revolutionary approach to AI education assessment that creates authentic value for learners while accurately measuring their competencies and growth. Unlike traditional testing approaches, portfolio development integrates assessment seamlessly into the learning process, ensuring that every assessment activity contributes directly to learners' professional development and career advancement.

Portfolio development in the SHE IS AI framework is based on the principle of authentic assessment, where learners demonstrate their competencies through real-world applications that have genuine value beyond the educational context. This approach recognizes that AI competencies are best demonstrated through practical application rather than abstract testing, and that assessment should create value for learners rather than simply measuring their knowledge.

The framework requires that all portfolio components meet three essential criteria: professional relevance, bias awareness integration, and collaborative development. Professional relevance ensures that portfolio components directly connect to career opportunities and professional requirements in AI-related fields. Bias awareness integration requires that all portfolio components explicitly address bias recognition, mitigation, or inclusive design considerations. Collaborative development emphasizes that portfolio components should demonstrate learners' ability to work effectively with diverse teams and stakeholders.

Portfolio components are organized around five core competency areas that reflect the essential skills and knowledge required for successful AI careers. The first competency area, Technical AI Literacy, includes portfolio components that demonstrate understanding of AI concepts, algorithms, and applications. These components might include technical reports, algorithm implementations, or system design proposals that show both technical competency and awareness of social implications.

The second competency area, Ethical AI Practice, requires portfolio components that demonstrate ability to identify, analyze, and address ethical considerations in AI development and deployment. These components might include ethical impact assessments, bias audits of existing systems, or proposals for ethical AI governance frameworks. All components in this area must demonstrate sophisticated understanding of ethical principles and practical skills for ethical implementation.

The third competency area, Inclusive AI Design, focuses on portfolio components that demonstrate ability to design and develop AI systems that serve diverse users and communities. These components might include user research reports, inclusive design proposals, or accessibility assessments that show understanding of diverse user needs and practical skills for inclusive development.

The fourth competency area, AI Communication and Advocacy, includes portfolio components that demonstrate ability to communicate about AI with diverse audiences and advocate for responsible AI practices. These components might include public presentations, policy briefs, or community education materials that show both technical understanding and communication skills.

The fifth competency area, Collaborative AI Development, requires portfolio components that demonstrate ability to work effectively in diverse teams on AI projects. These components might include team project reports, peer collaboration reflections, or leadership case studies that show both technical contribution and collaborative skills.

Each portfolio component includes detailed reflection requirements where learners analyze their learning process, identify areas for continued growth, and connect their work to broader career goals. These reflections are essential for developing metacognitive skills and ensuring that learners can articulate their competencies to potential employers, collaborators, and professional communities.

The framework includes comprehensive peer review processes where learners provide feedback on each other's portfolio components. These peer review processes serve multiple functions: they provide valuable feedback for portfolio improvement, they develop learners' ability to evaluate AI work critically, and they create opportunities for collaborative learning and professional networking.

Portfolio development is supported by extensive mentorship and feedback systems that connect learners with AI professionals, educators, and community members. These mentorship relationships provide guidance on portfolio development, career planning, and professional development while creating valuable networking opportunities for learners.

The framework includes specific requirements for portfolio accessibility and inclusive design, ensuring that all portfolio components are accessible to diverse audiences and demonstrate learners' commitment to inclusive practice. This includes requirements for alternative text, clear language, multiple format options, and cultural responsiveness in portfolio presentation.

Portfolio assessment uses rubrics that emphasize growth, improvement, and professional development rather than comparative ranking. These rubrics focus on evidence of learning, quality of reflection, professional relevance, and demonstration of framework values including bias awareness and inclusive practice.

The Portfolio Development component concludes with comprehensive portfolio presentation processes where learners share their work with authentic audiences including potential employers, community members, and professional colleagues. These presentations provide valuable experience in professional communication while creating opportunities for career advancement and professional networking."""
    },
    {
        "chunk_id": "facilitator_training_001",
        "category": "Facilitator Training",
        "educational_level": "Facilitator",
        "content_type": "Training Framework",
        "content": """The Facilitator Training and Support Framework represents a comprehensive approach to preparing educators to implement the SHE IS AI framework effectively while maintaining its core values of equity, inclusion, and bias elimination. This framework recognizes that successful implementation requires not only technical knowledge of AI concepts but also sophisticated understanding of inclusive pedagogy, bias-aware teaching practices, and culturally responsive education.

Facilitator preparation begins with intensive training in bias recognition and mitigation that goes far beyond traditional diversity training to provide practical skills for identifying and addressing bias in educational content, teaching practices, and learning environments. This training includes examination of implicit bias, structural bias, and systemic bias as they appear in educational contexts, with specific attention to how these biases affect AI education and career preparation.

The training framework includes comprehensive preparation in inclusive pedagogy that enables facilitators to create learning environments where all participants can succeed regardless of their background, learning style, or prior experience. This preparation includes understanding of Universal Design for Learning principles, culturally responsive teaching practices, and trauma-informed education approaches that recognize the diverse experiences and needs of AI learners.

Technical AI competency development receives significant attention, with facilitators required to demonstrate sophisticated understanding of AI concepts, applications, and implications. However, this technical preparation is always integrated with pedagogical preparation, ensuring that facilitators can not only understand AI concepts but also teach them effectively to diverse learners. The framework emphasizes that technical expertise alone is insufficient for effective AI education.

The training framework includes extensive preparation in assessment and portfolio development that enables facilitators to implement authentic assessment practices effectively. This preparation includes understanding of portfolio assessment principles, rubric development, peer review facilitation, and feedback provision that supports learner growth and professional development.

Community building skills receive explicit attention, with facilitators learning specific strategies for creating inclusive learning communities, facilitating difficult conversations about bias and equity, and supporting collaborative learning among diverse participants. This preparation includes understanding of group dynamics, conflict resolution, and community agreement development that supports the framework's collaborative learning approach.

The framework includes comprehensive preparation in cultural responsiveness that enables facilitators to adapt the framework appropriately for different cultural contexts while maintaining its core principles and values. This preparation includes understanding of different cultural approaches to learning, communication, and technology, with practical skills for culturally appropriate adaptation.

Professional development support includes ongoing mentorship, peer collaboration, and continuing education opportunities that ensure facilitators continue to grow and improve throughout their careers. This support recognizes that effective AI education requires continuous learning and adaptation as the field evolves and as facilitators gain experience with diverse learners and contexts.

The training framework includes specific preparation in ethical AI education that enables facilitators to guide learners through complex ethical considerations while maintaining appropriate boundaries and avoiding indoctrination. This preparation includes understanding of different ethical frameworks, strategies for facilitating ethical reasoning, and approaches to handling controversial or sensitive topics in AI education.

Quality assurance mechanisms ensure that facilitator training maintains high standards while remaining accessible to diverse educators. These mechanisms include competency assessments, peer review processes, and ongoing evaluation that supports continuous improvement in facilitator preparation and support.

The framework includes specific attention to facilitator well-being and sustainability, recognizing that effective AI education requires significant emotional and intellectual labor. Support systems include stress management resources, peer support networks, and workload management strategies that help facilitators maintain effectiveness while avoiding burnout.

Facilitator training concludes with comprehensive certification processes that verify facilitators' readiness to implement the SHE IS AI framework effectively. These certification processes include demonstration of technical competency, pedagogical skills, bias awareness, and commitment to the framework's values and principles."""
    },
    {
        "chunk_id": "quality_assurance_001",
        "category": "Quality Assurance",
        "educational_level": "Institutional",
        "content_type": "Quality Framework",
        "content": """The Quality Assurance and Continuous Improvement framework ensures that SHE IS AI implementation maintains high standards of educational effectiveness while continuously evolving to meet changing needs and incorporate emerging best practices. This framework recognizes that quality in AI education requires ongoing attention to both educational outcomes and equity impacts, with systematic processes for evaluation, feedback, and improvement.

Quality assurance begins with comprehensive outcome measurement that goes beyond traditional educational metrics to include measures of bias reduction, inclusive practice, career preparation, and community impact. These measures recognize that successful AI education must prepare learners for career success while contributing to more equitable and inclusive AI development practices.

The framework includes systematic data collection processes that gather information from multiple stakeholders including learners, facilitators, employers, and community members. This multi-stakeholder approach ensures that quality assessment reflects diverse perspectives and priorities while maintaining focus on the framework's core values and objectives.

Learner outcome measurement includes both immediate learning assessment and long-term career tracking that follows learners into their professional careers. This long-term tracking provides essential feedback about the framework's effectiveness in preparing learners for career success while identifying areas for improvement and adaptation.

Bias impact assessment receives specific attention, with systematic evaluation of how framework implementation affects different groups of learners and whether the framework successfully reduces bias and promotes inclusion in AI education and careers. This assessment includes both quantitative measures of participation and outcomes and qualitative evaluation of learner experiences and perceptions.

The framework includes comprehensive facilitator evaluation processes that assess both technical competency and inclusive teaching practice. These evaluations provide feedback for individual facilitator development while identifying systemic issues that require framework modification or additional training and support.

Institutional assessment examines how different educational institutions and contexts implement the framework, identifying factors that support or hinder successful implementation. This assessment provides guidance for institutional adaptation while maintaining framework integrity and effectiveness.

Community impact evaluation assesses how framework implementation affects broader communities, including impacts on local AI development, workforce diversity, and community engagement with AI technology. This evaluation recognizes that effective AI education should benefit not only individual learners but also their broader communities.

The framework includes systematic processes for incorporating feedback and evaluation results into framework improvement. These processes ensure that evaluation leads to concrete improvements rather than simply generating reports, with clear mechanisms for translating evaluation findings into framework modifications.

Continuous improvement processes include regular review cycles that examine all framework components for effectiveness, relevance, and alignment with evolving best practices in AI education and inclusive pedagogy. These review cycles involve multiple stakeholders and result in specific improvement plans with clear timelines and accountability mechanisms.

The framework includes processes for incorporating emerging research and best practices from AI education, inclusive pedagogy, and bias mitigation. These processes ensure that the framework remains current with evolving understanding while maintaining its core principles and proven effective practices.

Innovation and experimentation receive explicit support, with processes for piloting new approaches, evaluating their effectiveness, and incorporating successful innovations into the broader framework. This support for innovation ensures that the framework continues to evolve and improve while maintaining quality and consistency.

Quality assurance concludes with comprehensive reporting processes that share evaluation findings and improvement efforts with stakeholders, contributing to broader knowledge about effective AI education and inclusive pedagogy. These reporting processes support transparency and accountability while contributing to the broader educational community's understanding of effective AI education practices."""
    }
]

def upload_chunk(chunk):
    """Upload a single chunk to Supabase with embedding"""
    try:
        # Generate embedding
        embedding = get_embedding(chunk["content"])
        
        # Prepare metadata
        metadata = {
            "chunk_id": chunk["chunk_id"],
            "category": chunk["category"],
            "educational_level": chunk["educational_level"],
            "content_type": chunk["content_type"],
            "author": "Lenise Kenney",
            "framework": "SHE IS AI"
        }
        
        # Insert into Supabase
        result = supabase.table('framework_chunks').insert({
            'content': chunk["content"],
            'metadata': metadata,
            'embedding': embedding
        }).execute()
        
        print(f"✅ Uploaded: {chunk['chunk_id']}")
        return result
        
    except Exception as e:
        print(f"❌ Error uploading {chunk['chunk_id']}: {str(e)}")
        return None

def upload_all_chunks():
    """Upload all chunks to Supabase"""
    print("🚀 Starting framework vectorization...")
    print(f"📝 Total chunks to process: {len(chunks)}")
    
    successful_uploads = 0
    failed_uploads = 0
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n📤 Processing chunk {i}/{len(chunks)}: {chunk['chunk_id']}")
        
        result = upload_chunk(chunk)
        if result:
            successful_uploads += 1
        else:
            failed_uploads += 1
    
    print(f"\n🎉 Vectorization complete!")
    print(f"✅ Successful uploads: {successful_uploads}")
    print(f"❌ Failed uploads: {failed_uploads}")
    
    if failed_uploads == 0:
        print("🚀 Your SHE IS AI framework is now vectorized and ready for RAG!")

def test_similarity_search(query="bias in AI education"):
    """Test the similarity search functionality"""
    try:
        # Generate embedding for query
        query_embedding = get_embedding(query)
        
        # Search for similar chunks using cosine similarity
        result = supabase.rpc('match_framework_chunks_hf', {
            'query_embedding': query_embedding,
            'match_threshold': 0.3,  # Lower threshold for Hugging Face embeddings
            'match_count': 3
        }).execute()
        
        print(f"\n🔍 Test search for: '{query}'")
        print(f"Found {len(result.data)} relevant chunks:")
        
        for i, match in enumerate(result.data, 1):
            print(f"\n{i}. {match['metadata']['chunk_id']}")
            print(f"   Similarity: {match.get('similarity', 'N/A'):.3f}")
            print(f"   Category: {match['metadata']['category']}")
            print(f"   Content: {match['content'][:150]}...")
            
    except Exception as e:
        print(f"❌ Error testing search: {str(e)}")
        print("Note: You may need to create the search function in Supabase first.")

if __name__ == "__main__":
    print("SHE IS AI Framework Vectorization Script")
    print("Created by: Lenise Kenney")
    print("Using Hugging Face Embeddings (Free!)")
    print("="*60)
    
    # Upload all chunks
    upload_all_chunks()
    
    # Test the search functionality
    test_similarity_search()