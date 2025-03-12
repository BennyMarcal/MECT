// Generated from c:/Users/benny/Desktop/ECT/4º Ano/2 Semestre/C/test/agl.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class aglParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, ID=24, Number=25, 
		Integer=26, String=27, WS=28, COMMENT=29, MULTICOMMENT=30, ERROR=31;
	public static final int
		RULE_program = 0, RULE_stat = 1, RULE_assign = 2, RULE_instantiation = 3, 
		RULE_dataType = 4, RULE_action = 5, RULE_figureDef = 6, RULE_viewDef = 7, 
		RULE_loopDef = 8, RULE_dataPoint = 9;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "stat", "assign", "instantiation", "dataType", "action", "figureDef", 
			"viewDef", "loopDef", "dataPoint"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "';'", "'='", "':'", "'-'", "'+'", "'('", "','", "')'", "'close'", 
			"'refresh'", "'after'", "'ms'", "'s'", "'print'", "'wait mouse click'", 
			"'at'", "'with'", "'{'", "'}'", "'for'", "'in'", "'..'", "'do'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			"ID", "Number", "Integer", "String", "WS", "COMMENT", "MULTICOMMENT", 
			"ERROR"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "agl.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public aglParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(aglParser.EOF, 0); }
		public List<StatContext> stat() {
			return getRuleContexts(StatContext.class);
		}
		public StatContext stat(int i) {
			return getRuleContext(StatContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(23);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 17876480L) != 0)) {
				{
				{
				setState(20);
				stat();
				}
				}
				setState(25);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(26);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StatContext extends ParserRuleContext {
		public StatContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_stat; }
	 
		public StatContext() { }
		public void copyFrom(StatContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StatInstantiationContext extends StatContext {
		public InstantiationContext instantiation() {
			return getRuleContext(InstantiationContext.class,0);
		}
		public StatInstantiationContext(StatContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StatViewContext extends StatContext {
		public ViewDefContext viewDef() {
			return getRuleContext(ViewDefContext.class,0);
		}
		public StatViewContext(StatContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StatActionContext extends StatContext {
		public ActionContext action() {
			return getRuleContext(ActionContext.class,0);
		}
		public StatActionContext(StatContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StatFigureContext extends StatContext {
		public FigureDefContext figureDef() {
			return getRuleContext(FigureDefContext.class,0);
		}
		public StatFigureContext(StatContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StatAssignContext extends StatContext {
		public AssignContext assign() {
			return getRuleContext(AssignContext.class,0);
		}
		public StatAssignContext(StatContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StatLoopContext extends StatContext {
		public LoopDefContext loopDef() {
			return getRuleContext(LoopDefContext.class,0);
		}
		public StatLoopContext(StatContext ctx) { copyFrom(ctx); }
	}

	public final StatContext stat() throws RecognitionException {
		StatContext _localctx = new StatContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_stat);
		try {
			setState(40);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
			case 1:
				_localctx = new StatInstantiationContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(28);
				instantiation();
				setState(29);
				match(T__0);
				}
				break;
			case 2:
				_localctx = new StatAssignContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(31);
				assign();
				setState(32);
				match(T__0);
				}
				break;
			case 3:
				_localctx = new StatActionContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(34);
				action();
				setState(35);
				match(T__0);
				}
				break;
			case 4:
				_localctx = new StatViewContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(37);
				viewDef();
				}
				break;
			case 5:
				_localctx = new StatFigureContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(38);
				figureDef();
				}
				break;
			case 6:
				_localctx = new StatLoopContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(39);
				loopDef();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AssignContext extends ParserRuleContext {
		public AssignContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assign; }
	 
		public AssignContext() { }
		public void copyFrom(AssignContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AssignExistingContext extends AssignContext {
		public TerminalNode ID() { return getToken(aglParser.ID, 0); }
		public DataTypeContext dataType() {
			return getRuleContext(DataTypeContext.class,0);
		}
		public AssignExistingContext(AssignContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AssignInstantiationContext extends AssignContext {
		public InstantiationContext instantiation() {
			return getRuleContext(InstantiationContext.class,0);
		}
		public DataTypeContext dataType() {
			return getRuleContext(DataTypeContext.class,0);
		}
		public AssignInstantiationContext(AssignContext ctx) { copyFrom(ctx); }
	}

	public final AssignContext assign() throws RecognitionException {
		AssignContext _localctx = new AssignContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_assign);
		try {
			setState(49);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
			case 1:
				_localctx = new AssignExistingContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(42);
				match(ID);
				setState(43);
				match(T__1);
				setState(44);
				dataType();
				}
				break;
			case 2:
				_localctx = new AssignInstantiationContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(45);
				instantiation();
				setState(46);
				match(T__1);
				setState(47);
				dataType();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstantiationContext extends ParserRuleContext {
		public InstantiationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instantiation; }
	 
		public InstantiationContext() { }
		public void copyFrom(InstantiationContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class InstantiationDefContext extends InstantiationContext {
		public List<TerminalNode> ID() { return getTokens(aglParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(aglParser.ID, i);
		}
		public InstantiationDefContext(InstantiationContext ctx) { copyFrom(ctx); }
	}

	public final InstantiationContext instantiation() throws RecognitionException {
		InstantiationContext _localctx = new InstantiationContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_instantiation);
		try {
			_localctx = new InstantiationDefContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(51);
			match(ID);
			setState(52);
			match(T__2);
			setState(53);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeContext extends ParserRuleContext {
		public DataTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_dataType; }
	 
		public DataTypeContext() { }
		public void copyFrom(DataTypeContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeUnaryContext extends DataTypeContext {
		public Token op;
		public DataTypeContext dataType() {
			return getRuleContext(DataTypeContext.class,0);
		}
		public DataTypeUnaryContext(DataTypeContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeStringContext extends DataTypeContext {
		public TerminalNode String() { return getToken(aglParser.String, 0); }
		public DataTypeStringContext(DataTypeContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeActionContext extends DataTypeContext {
		public ActionContext action() {
			return getRuleContext(ActionContext.class,0);
		}
		public DataTypeActionContext(DataTypeContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypePointContext extends DataTypeContext {
		public List<DataTypeContext> dataType() {
			return getRuleContexts(DataTypeContext.class);
		}
		public DataTypeContext dataType(int i) {
			return getRuleContext(DataTypeContext.class,i);
		}
		public DataTypePointContext(DataTypeContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeRealNumberContext extends DataTypeContext {
		public TerminalNode Number() { return getToken(aglParser.Number, 0); }
		public DataTypeRealNumberContext(DataTypeContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeIDContext extends DataTypeContext {
		public TerminalNode ID() { return getToken(aglParser.ID, 0); }
		public DataTypeIDContext(DataTypeContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeIntegerContext extends DataTypeContext {
		public TerminalNode Integer() { return getToken(aglParser.Integer, 0); }
		public DataTypeIntegerContext(DataTypeContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataTypeVectorContext extends DataTypeContext {
		public List<TerminalNode> Number() { return getTokens(aglParser.Number); }
		public TerminalNode Number(int i) {
			return getToken(aglParser.Number, i);
		}
		public DataTypeVectorContext(DataTypeContext ctx) { copyFrom(ctx); }
	}

	public final DataTypeContext dataType() throws RecognitionException {
		DataTypeContext _localctx = new DataTypeContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_dataType);
		int _la;
		try {
			setState(73);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
			case 1:
				_localctx = new DataTypeUnaryContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(55);
				((DataTypeUnaryContext)_localctx).op = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__3 || _la==T__4) ) {
					((DataTypeUnaryContext)_localctx).op = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(56);
				dataType();
				}
				break;
			case 2:
				_localctx = new DataTypePointContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(57);
				match(T__5);
				setState(58);
				dataType();
				setState(59);
				match(T__6);
				setState(60);
				dataType();
				setState(61);
				match(T__7);
				}
				break;
			case 3:
				_localctx = new DataTypeVectorContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(63);
				match(T__5);
				setState(64);
				match(Number);
				setState(65);
				_la = _input.LA(1);
				if ( !(_la==T__2 || _la==T__6) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(66);
				match(Number);
				setState(67);
				match(T__7);
				}
				break;
			case 4:
				_localctx = new DataTypeRealNumberContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(68);
				match(Number);
				}
				break;
			case 5:
				_localctx = new DataTypeStringContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(69);
				match(String);
				}
				break;
			case 6:
				_localctx = new DataTypeActionContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(70);
				action();
				}
				break;
			case 7:
				_localctx = new DataTypeIDContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(71);
				match(ID);
				}
				break;
			case 8:
				_localctx = new DataTypeIntegerContext(_localctx);
				enterOuterAlt(_localctx, 8);
				{
				setState(72);
				match(Integer);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ActionContext extends ParserRuleContext {
		public ActionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_action; }
	 
		public ActionContext() { }
		public void copyFrom(ActionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ActionRefreshContext extends ActionContext {
		public TerminalNode ID() { return getToken(aglParser.ID, 0); }
		public TerminalNode Integer() { return getToken(aglParser.Integer, 0); }
		public ActionRefreshContext(ActionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ActionCloseContext extends ActionContext {
		public TerminalNode ID() { return getToken(aglParser.ID, 0); }
		public ActionCloseContext(ActionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ActionPrintContext extends ActionContext {
		public List<TerminalNode> String() { return getTokens(aglParser.String); }
		public TerminalNode String(int i) {
			return getToken(aglParser.String, i);
		}
		public List<TerminalNode> ID() { return getTokens(aglParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(aglParser.ID, i);
		}
		public ActionPrintContext(ActionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ActionMouseContext extends ActionContext {
		public ActionMouseContext(ActionContext ctx) { copyFrom(ctx); }
	}

	public final ActionContext action() throws RecognitionException {
		ActionContext _localctx = new ActionContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_action);
		int _la;
		try {
			setState(91);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__8:
				_localctx = new ActionCloseContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(75);
				match(T__8);
				setState(76);
				match(ID);
				}
				break;
			case T__9:
				_localctx = new ActionRefreshContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(77);
				match(T__9);
				setState(78);
				match(ID);
				setState(82);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__10) {
					{
					setState(79);
					match(T__10);
					setState(80);
					match(Integer);
					setState(81);
					_la = _input.LA(1);
					if ( !(_la==T__11 || _la==T__12) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
				}

				}
				break;
			case T__13:
				_localctx = new ActionPrintContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(84);
				match(T__13);
				setState(86); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(85);
					_la = _input.LA(1);
					if ( !(_la==ID || _la==String) ) {
					_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					}
					}
					setState(88); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==ID || _la==String );
				}
				break;
			case T__14:
				_localctx = new ActionMouseContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(90);
				match(T__14);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FigureDefContext extends ParserRuleContext {
		public FigureDefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_figureDef; }
	 
		public FigureDefContext() { }
		public void copyFrom(FigureDefContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FigureDefinitionContext extends FigureDefContext {
		public DataPointContext dataPoint() {
			return getRuleContext(DataPointContext.class,0);
		}
		public TerminalNode ID() { return getToken(aglParser.ID, 0); }
		public InstantiationContext instantiation() {
			return getRuleContext(InstantiationContext.class,0);
		}
		public List<AssignContext> assign() {
			return getRuleContexts(AssignContext.class);
		}
		public AssignContext assign(int i) {
			return getRuleContext(AssignContext.class,i);
		}
		public FigureDefinitionContext(FigureDefContext ctx) { copyFrom(ctx); }
	}

	public final FigureDefContext figureDef() throws RecognitionException {
		FigureDefContext _localctx = new FigureDefContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_figureDef);
		int _la;
		try {
			_localctx = new FigureDefinitionContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(95);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,7,_ctx) ) {
			case 1:
				{
				setState(93);
				match(ID);
				}
				break;
			case 2:
				{
				setState(94);
				instantiation();
				}
				break;
			}
			setState(97);
			match(T__15);
			setState(98);
			dataPoint();
			setState(99);
			match(T__16);
			setState(100);
			match(T__17);
			setState(106);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==ID) {
				{
				{
				setState(101);
				assign();
				setState(102);
				match(T__0);
				}
				}
				setState(108);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(109);
			match(T__18);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ViewDefContext extends ParserRuleContext {
		public ViewDefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_viewDef; }
	 
		public ViewDefContext() { }
		public void copyFrom(ViewDefContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ViewDefinitionContext extends ViewDefContext {
		public InstantiationContext instantiation() {
			return getRuleContext(InstantiationContext.class,0);
		}
		public List<AssignContext> assign() {
			return getRuleContexts(AssignContext.class);
		}
		public AssignContext assign(int i) {
			return getRuleContext(AssignContext.class,i);
		}
		public ViewDefinitionContext(ViewDefContext ctx) { copyFrom(ctx); }
	}

	public final ViewDefContext viewDef() throws RecognitionException {
		ViewDefContext _localctx = new ViewDefContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_viewDef);
		int _la;
		try {
			_localctx = new ViewDefinitionContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(111);
			instantiation();
			setState(112);
			match(T__16);
			setState(113);
			match(T__17);
			setState(119);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==ID) {
				{
				{
				setState(114);
				assign();
				setState(115);
				match(T__0);
				}
				}
				setState(121);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(122);
			match(T__18);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LoopDefContext extends ParserRuleContext {
		public LoopDefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_loopDef; }
	 
		public LoopDefContext() { }
		public void copyFrom(LoopDefContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LoopDefinitionContext extends LoopDefContext {
		public TerminalNode ID() { return getToken(aglParser.ID, 0); }
		public List<TerminalNode> Integer() { return getTokens(aglParser.Integer); }
		public TerminalNode Integer(int i) {
			return getToken(aglParser.Integer, i);
		}
		public List<StatContext> stat() {
			return getRuleContexts(StatContext.class);
		}
		public StatContext stat(int i) {
			return getRuleContext(StatContext.class,i);
		}
		public LoopDefinitionContext(LoopDefContext ctx) { copyFrom(ctx); }
	}

	public final LoopDefContext loopDef() throws RecognitionException {
		LoopDefContext _localctx = new LoopDefContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_loopDef);
		int _la;
		try {
			_localctx = new LoopDefinitionContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(124);
			match(T__19);
			setState(125);
			match(ID);
			setState(126);
			match(T__20);
			setState(127);
			match(Integer);
			setState(128);
			match(T__21);
			setState(129);
			match(Integer);
			setState(132);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__21) {
				{
				setState(130);
				match(T__21);
				setState(131);
				match(Integer);
				}
			}

			setState(134);
			match(T__22);
			setState(135);
			match(T__17);
			setState(139);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 17876480L) != 0)) {
				{
				{
				setState(136);
				stat();
				}
				}
				setState(141);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(142);
			match(T__18);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DataPointContext extends ParserRuleContext {
		public DataPointContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_dataPoint; }
	 
		public DataPointContext() { }
		public void copyFrom(DataPointContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DataPointDefContext extends DataPointContext {
		public List<DataTypeContext> dataType() {
			return getRuleContexts(DataTypeContext.class);
		}
		public DataTypeContext dataType(int i) {
			return getRuleContext(DataTypeContext.class,i);
		}
		public DataPointDefContext(DataPointContext ctx) { copyFrom(ctx); }
	}

	public final DataPointContext dataPoint() throws RecognitionException {
		DataPointContext _localctx = new DataPointContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_dataPoint);
		try {
			_localctx = new DataPointDefContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(144);
			match(T__5);
			setState(145);
			dataType();
			setState(146);
			match(T__6);
			setState(147);
			dataType();
			setState(148);
			match(T__7);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u001f\u0097\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001"+
		"\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004"+
		"\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007"+
		"\u0002\b\u0007\b\u0002\t\u0007\t\u0001\u0000\u0005\u0000\u0016\b\u0000"+
		"\n\u0000\f\u0000\u0019\t\u0000\u0001\u0000\u0001\u0000\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003\u0001)\b"+
		"\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0001\u0002\u0003\u00022\b\u0002\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0003\u0004J\b\u0004\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005S\b"+
		"\u0005\u0001\u0005\u0001\u0005\u0004\u0005W\b\u0005\u000b\u0005\f\u0005"+
		"X\u0001\u0005\u0003\u0005\\\b\u0005\u0001\u0006\u0001\u0006\u0003\u0006"+
		"`\b\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0006\u0001\u0006\u0005\u0006i\b\u0006\n\u0006\f\u0006l\t\u0006"+
		"\u0001\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007"+
		"\u0001\u0007\u0001\u0007\u0005\u0007v\b\u0007\n\u0007\f\u0007y\t\u0007"+
		"\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001"+
		"\b\u0001\b\u0001\b\u0003\b\u0085\b\b\u0001\b\u0001\b\u0001\b\u0005\b\u008a"+
		"\b\b\n\b\f\b\u008d\t\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0001\t"+
		"\u0001\t\u0001\t\u0001\t\u0000\u0000\n\u0000\u0002\u0004\u0006\b\n\f\u000e"+
		"\u0010\u0012\u0000\u0004\u0001\u0000\u0004\u0005\u0002\u0000\u0003\u0003"+
		"\u0007\u0007\u0001\u0000\f\r\u0002\u0000\u0018\u0018\u001b\u001b\u00a4"+
		"\u0000\u0017\u0001\u0000\u0000\u0000\u0002(\u0001\u0000\u0000\u0000\u0004"+
		"1\u0001\u0000\u0000\u0000\u00063\u0001\u0000\u0000\u0000\bI\u0001\u0000"+
		"\u0000\u0000\n[\u0001\u0000\u0000\u0000\f_\u0001\u0000\u0000\u0000\u000e"+
		"o\u0001\u0000\u0000\u0000\u0010|\u0001\u0000\u0000\u0000\u0012\u0090\u0001"+
		"\u0000\u0000\u0000\u0014\u0016\u0003\u0002\u0001\u0000\u0015\u0014\u0001"+
		"\u0000\u0000\u0000\u0016\u0019\u0001\u0000\u0000\u0000\u0017\u0015\u0001"+
		"\u0000\u0000\u0000\u0017\u0018\u0001\u0000\u0000\u0000\u0018\u001a\u0001"+
		"\u0000\u0000\u0000\u0019\u0017\u0001\u0000\u0000\u0000\u001a\u001b\u0005"+
		"\u0000\u0000\u0001\u001b\u0001\u0001\u0000\u0000\u0000\u001c\u001d\u0003"+
		"\u0006\u0003\u0000\u001d\u001e\u0005\u0001\u0000\u0000\u001e)\u0001\u0000"+
		"\u0000\u0000\u001f \u0003\u0004\u0002\u0000 !\u0005\u0001\u0000\u0000"+
		"!)\u0001\u0000\u0000\u0000\"#\u0003\n\u0005\u0000#$\u0005\u0001\u0000"+
		"\u0000$)\u0001\u0000\u0000\u0000%)\u0003\u000e\u0007\u0000&)\u0003\f\u0006"+
		"\u0000\')\u0003\u0010\b\u0000(\u001c\u0001\u0000\u0000\u0000(\u001f\u0001"+
		"\u0000\u0000\u0000(\"\u0001\u0000\u0000\u0000(%\u0001\u0000\u0000\u0000"+
		"(&\u0001\u0000\u0000\u0000(\'\u0001\u0000\u0000\u0000)\u0003\u0001\u0000"+
		"\u0000\u0000*+\u0005\u0018\u0000\u0000+,\u0005\u0002\u0000\u0000,2\u0003"+
		"\b\u0004\u0000-.\u0003\u0006\u0003\u0000./\u0005\u0002\u0000\u0000/0\u0003"+
		"\b\u0004\u000002\u0001\u0000\u0000\u00001*\u0001\u0000\u0000\u00001-\u0001"+
		"\u0000\u0000\u00002\u0005\u0001\u0000\u0000\u000034\u0005\u0018\u0000"+
		"\u000045\u0005\u0003\u0000\u000056\u0005\u0018\u0000\u00006\u0007\u0001"+
		"\u0000\u0000\u000078\u0007\u0000\u0000\u00008J\u0003\b\u0004\u00009:\u0005"+
		"\u0006\u0000\u0000:;\u0003\b\u0004\u0000;<\u0005\u0007\u0000\u0000<=\u0003"+
		"\b\u0004\u0000=>\u0005\b\u0000\u0000>J\u0001\u0000\u0000\u0000?@\u0005"+
		"\u0006\u0000\u0000@A\u0005\u0019\u0000\u0000AB\u0007\u0001\u0000\u0000"+
		"BC\u0005\u0019\u0000\u0000CJ\u0005\b\u0000\u0000DJ\u0005\u0019\u0000\u0000"+
		"EJ\u0005\u001b\u0000\u0000FJ\u0003\n\u0005\u0000GJ\u0005\u0018\u0000\u0000"+
		"HJ\u0005\u001a\u0000\u0000I7\u0001\u0000\u0000\u0000I9\u0001\u0000\u0000"+
		"\u0000I?\u0001\u0000\u0000\u0000ID\u0001\u0000\u0000\u0000IE\u0001\u0000"+
		"\u0000\u0000IF\u0001\u0000\u0000\u0000IG\u0001\u0000\u0000\u0000IH\u0001"+
		"\u0000\u0000\u0000J\t\u0001\u0000\u0000\u0000KL\u0005\t\u0000\u0000L\\"+
		"\u0005\u0018\u0000\u0000MN\u0005\n\u0000\u0000NR\u0005\u0018\u0000\u0000"+
		"OP\u0005\u000b\u0000\u0000PQ\u0005\u001a\u0000\u0000QS\u0007\u0002\u0000"+
		"\u0000RO\u0001\u0000\u0000\u0000RS\u0001\u0000\u0000\u0000S\\\u0001\u0000"+
		"\u0000\u0000TV\u0005\u000e\u0000\u0000UW\u0007\u0003\u0000\u0000VU\u0001"+
		"\u0000\u0000\u0000WX\u0001\u0000\u0000\u0000XV\u0001\u0000\u0000\u0000"+
		"XY\u0001\u0000\u0000\u0000Y\\\u0001\u0000\u0000\u0000Z\\\u0005\u000f\u0000"+
		"\u0000[K\u0001\u0000\u0000\u0000[M\u0001\u0000\u0000\u0000[T\u0001\u0000"+
		"\u0000\u0000[Z\u0001\u0000\u0000\u0000\\\u000b\u0001\u0000\u0000\u0000"+
		"]`\u0005\u0018\u0000\u0000^`\u0003\u0006\u0003\u0000_]\u0001\u0000\u0000"+
		"\u0000_^\u0001\u0000\u0000\u0000`a\u0001\u0000\u0000\u0000ab\u0005\u0010"+
		"\u0000\u0000bc\u0003\u0012\t\u0000cd\u0005\u0011\u0000\u0000dj\u0005\u0012"+
		"\u0000\u0000ef\u0003\u0004\u0002\u0000fg\u0005\u0001\u0000\u0000gi\u0001"+
		"\u0000\u0000\u0000he\u0001\u0000\u0000\u0000il\u0001\u0000\u0000\u0000"+
		"jh\u0001\u0000\u0000\u0000jk\u0001\u0000\u0000\u0000km\u0001\u0000\u0000"+
		"\u0000lj\u0001\u0000\u0000\u0000mn\u0005\u0013\u0000\u0000n\r\u0001\u0000"+
		"\u0000\u0000op\u0003\u0006\u0003\u0000pq\u0005\u0011\u0000\u0000qw\u0005"+
		"\u0012\u0000\u0000rs\u0003\u0004\u0002\u0000st\u0005\u0001\u0000\u0000"+
		"tv\u0001\u0000\u0000\u0000ur\u0001\u0000\u0000\u0000vy\u0001\u0000\u0000"+
		"\u0000wu\u0001\u0000\u0000\u0000wx\u0001\u0000\u0000\u0000xz\u0001\u0000"+
		"\u0000\u0000yw\u0001\u0000\u0000\u0000z{\u0005\u0013\u0000\u0000{\u000f"+
		"\u0001\u0000\u0000\u0000|}\u0005\u0014\u0000\u0000}~\u0005\u0018\u0000"+
		"\u0000~\u007f\u0005\u0015\u0000\u0000\u007f\u0080\u0005\u001a\u0000\u0000"+
		"\u0080\u0081\u0005\u0016\u0000\u0000\u0081\u0084\u0005\u001a\u0000\u0000"+
		"\u0082\u0083\u0005\u0016\u0000\u0000\u0083\u0085\u0005\u001a\u0000\u0000"+
		"\u0084\u0082\u0001\u0000\u0000\u0000\u0084\u0085\u0001\u0000\u0000\u0000"+
		"\u0085\u0086\u0001\u0000\u0000\u0000\u0086\u0087\u0005\u0017\u0000\u0000"+
		"\u0087\u008b\u0005\u0012\u0000\u0000\u0088\u008a\u0003\u0002\u0001\u0000"+
		"\u0089\u0088\u0001\u0000\u0000\u0000\u008a\u008d\u0001\u0000\u0000\u0000"+
		"\u008b\u0089\u0001\u0000\u0000\u0000\u008b\u008c\u0001\u0000\u0000\u0000"+
		"\u008c\u008e\u0001\u0000\u0000\u0000\u008d\u008b\u0001\u0000\u0000\u0000"+
		"\u008e\u008f\u0005\u0013\u0000\u0000\u008f\u0011\u0001\u0000\u0000\u0000"+
		"\u0090\u0091\u0005\u0006\u0000\u0000\u0091\u0092\u0003\b\u0004\u0000\u0092"+
		"\u0093\u0005\u0007\u0000\u0000\u0093\u0094\u0003\b\u0004\u0000\u0094\u0095"+
		"\u0005\b\u0000\u0000\u0095\u0013\u0001\u0000\u0000\u0000\f\u0017(1IRX"+
		"[_jw\u0084\u008b";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}