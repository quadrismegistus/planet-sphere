from .base import *



class Txt(Base):
    __tablename__ = 'text'
    id: Mapped[int] = mapped_column(primary_key=True)
    txt: Mapped[str]
    lang: Mapped[Optional[str]]

    translations: Mapped[List['Translation']] = relationship(
        back_populates='text'
    )

    def to_dict(self):
        d=super().to_dict()
        d['translations']=[
            tr.data
            for tr in self.translations
        ]
        return d
    
    def translate_to(self, lang):
        if lang == self.lang: return self
        transl = Translation.get(text_id=self.id, lang=lang)
        if not transl:
            res = translate_text(lang, self.txt)
            transltext = res.get('translatedText')
            if transltext:
                transl = Translation(text_id=self.id,
                                     txt=transltext,
                                     lang=lang).save()
        return transl
    
    


class Translation(Base):
    __tablename__ = 'translation'
    id: Mapped[int] = mapped_column(primary_key=True)

    text_id: Mapped[int] = mapped_column(ForeignKey('text.id'))
    text: Mapped['Txt'] = relationship(
        back_populates='translations',
        foreign_keys=[text_id]
    )

    txt: Mapped[str]
    lang: Mapped[str]

    def __repr__(self):
        return f'Translation(id={self.id},  text_id={self.text_id}, lang="{self.lang}", text="{self.txt}")'
