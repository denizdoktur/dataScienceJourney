import asyncio
import logging
from typing import List
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from crewaiflowandcrews.crews.poem_crew.write_article_chapter_crew.write_article_chapter_crew import WriteArticleChapterCrew
from crewaiflowandcrews.types import Chapter, ChapterOutline
from .crews.poem_crew.outline_article_crew.outline_crew import OutlineCrew
# from langtrace_python_sdk import langtrace

# langtrace.init(api_key = '<LANGTRACE_API_KEY>')

# Logger yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ArticleFlow")

# ArticleState, makale üretim sürecinde input olarak kullanılacak verileri tanımlayan Pydantic modeli.
class ArticleState(BaseModel):
    # Makalenin başlığını içeren metin
    title: str = "The Role of Artificial Intelligence in Healthcare"
    # Oluşturulan makale bölümlerinin saklanacağı liste
    article: List[Chapter] = []
    # Makalenin bölümlerinin taslak bilgisini içeren liste
    article_outline: List[ChapterOutline] = []
    # Makalenin konusu
    topic: str = (
        "Exploring the transformative impact of artificial intelligence on the healthcare industry, from diagnostics to personalized treatment."
    )
    # Makalenin amacını açıklayan metin
    goal: str = """
        The goal of this article is to provide a comprehensive overview of how artificial intelligence is revolutionizing the healthcare sector.
        It will explore the latest innovations in medical AI, the challenges associated with integrating AI into clinical practice,
        and the potential future developments in the field. The article aims to offer insights for healthcare professionals,
        technologists, and policymakers, highlighting key breakthroughs, ethical considerations, and strategies for effective AI implementation.
    """

# outline_article_crew ve write_article_chapter_crew arasındaki koordinasyonu sağlayan Flow yapısı.
class ArticleFlow(Flow[ArticleState]):

    # Başlangıç adımı: Makale taslağını (outline) oluşturur.
    @start()
    def generate_article_outline(self):
        logger.info("Kickoff the Article Outline Crew")
        try:
            # OutlineCrew çağrılarak makale taslağı oluşturuluyor.
            output = (
                OutlineCrew()
                .crew()
                .kickoff(inputs={"topic": self.state.topic, "goal": self.state.goal})
            )
            # Oluşturulan taslaktaki bölümler alınıyor.
            chapters = output["chapters"]
            logger.info("Chapters generated: %s", chapters)
            # Durum (state) içine taslak bilgiler kaydediliyor.
            self.state.article_outline = chapters
        except Exception as e:
            logger.exception("Error generating article outline: %s", e)
            raise

    # generate_article_outline adımının tamamlanmasını dinleyen ve bölümleri oluşturan adım.
    @listen(generate_article_outline)
    async def write_chapters(self):
        logger.info("Writing Article Chapters")
        tasks = []

        # Her bir bölüm için ayrı bir asenkron görev tanımlanıyor.
        async def write_single_chapter(chapter_outline):
            try:
                # WriteArticleChapterCrew kullanılarak bölüm içeriği oluşturuluyor.
                output = (
                    WriteArticleChapterCrew()
                    .crew()
                    .kickoff(
                        inputs={
                            "goal": self.state.goal,
                            "topic": self.state.topic,
                            "chapter_title": chapter_outline.title,
                            "chapter_description": chapter_outline.description,
                            "article_outline": [
                                chapter_outline.model_dump_json()
                                for chapter_outline in self.state.article_outline
                            ],
                        }
                    )
                )
                # Oluşturulan bölüm başlığı ve içeriği alınıyor.
                title = output["title"]
                content = output["content"]
                chapter = Chapter(title=title, content=content)
                logger.info("Successfully wrote chapter: %s", title)
                return chapter
            except Exception as e:
                logger.exception("Error writing chapter %s: %s", chapter_outline.title, e)
                raise

        # Tüm bölüm taslakları için asenkron görevler oluşturuluyor.
        for chapter_outline in self.state.article_outline:
            logger.info("Writing Chapter: %s", chapter_outline.title)
            logger.debug("Chapter description: %s", chapter_outline.description)
            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        try:
            # Tüm bölüm oluşturma görevleri paralel şekilde bekleniyor.
            chapters = await asyncio.gather(*tasks)
            logger.info("Newly generated chapters: %s", chapters)
            # Oluşturulan bölümler, makale durumuna ekleniyor.
            self.state.article.extend(chapters)
            logger.info("Article Chapters updated: %s", self.state.article)
        except Exception as e:
            logger.exception("Error during writing chapters: %s", e)
            raise

    # Tüm oluşturulan bölümleri birleştirip dosyaya kaydeden adım.
    @listen(write_chapters)
    async def join_and_save_chapter(self):
        logger.info("Joining and Saving Article Chapters")
        try:
            article_content = ""
            # Her bölüm için başlık ve içerik markdown formatında ekleniyor.
            for chapter in self.state.article:
                article_content += f"# {chapter.title}\n\n"
                article_content += f"{chapter.content}\n\n"

            # Makale başlığından dosya adı oluşturuluyor.
            article_title = self.state.title
            filename = f"./{article_title.replace(' ', '_')}.md"

            # Dosya yazma işlemi gerçekleştiriliyor.
            with open(filename, "w", encoding="utf-8") as file:
                file.write(article_content)

            logger.info("Article saved as %s", filename)
        except Exception as e:
            logger.exception("Error joining and saving chapters: %s", e)
            raise

# Flow'u başlatan fonksiyon
def kickoff():
    try:
        flow = ArticleFlow()
        flow.kickoff()
    except Exception as e:
        logger.exception("Error in kickoff: %s", e)

# Plot'ı başlatan fonksiyon
def plot():
    try:
        flow = ArticleFlow()
        flow.plot()
    except Exception as e:
        logger.exception("Error in plot: %s", e)

# Kullanıcıdan gelen input değerleriyle Flow'u başlatan fonksiyon.
def kickoff_with_input(title: str, topic: str, goal: str):
    try:
        flow = ArticleFlow()
        flow.state.title = title
        flow.state.topic = topic
        flow.state.goal = goal
        flow.kickoff()
    except Exception as e:
        logger.exception("Error in kickoff_with_input: %s", e)
        raise

if __name__ == "__main__":
    kickoff()
