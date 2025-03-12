// Generated from agl.g4 by ANTLR 4.12.0
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link aglParser}.
 */
public interface aglListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link aglParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(aglParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link aglParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(aglParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by the {@code statInstantiation}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterStatInstantiation(aglParser.StatInstantiationContext ctx);
	/**
	 * Exit a parse tree produced by the {@code statInstantiation}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitStatInstantiation(aglParser.StatInstantiationContext ctx);
	/**
	 * Enter a parse tree produced by the {@code statAssign}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterStatAssign(aglParser.StatAssignContext ctx);
	/**
	 * Exit a parse tree produced by the {@code statAssign}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitStatAssign(aglParser.StatAssignContext ctx);
	/**
	 * Enter a parse tree produced by the {@code statAction}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterStatAction(aglParser.StatActionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code statAction}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitStatAction(aglParser.StatActionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code statView}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterStatView(aglParser.StatViewContext ctx);
	/**
	 * Exit a parse tree produced by the {@code statView}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitStatView(aglParser.StatViewContext ctx);
	/**
	 * Enter a parse tree produced by the {@code statFigure}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterStatFigure(aglParser.StatFigureContext ctx);
	/**
	 * Exit a parse tree produced by the {@code statFigure}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitStatFigure(aglParser.StatFigureContext ctx);
	/**
	 * Enter a parse tree produced by the {@code statLoop}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterStatLoop(aglParser.StatLoopContext ctx);
	/**
	 * Exit a parse tree produced by the {@code statLoop}
	 * labeled alternative in {@link aglParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitStatLoop(aglParser.StatLoopContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignExisting}
	 * labeled alternative in {@link aglParser#assign}.
	 * @param ctx the parse tree
	 */
	void enterAssignExisting(aglParser.AssignExistingContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignExisting}
	 * labeled alternative in {@link aglParser#assign}.
	 * @param ctx the parse tree
	 */
	void exitAssignExisting(aglParser.AssignExistingContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignInstantiation}
	 * labeled alternative in {@link aglParser#assign}.
	 * @param ctx the parse tree
	 */
	void enterAssignInstantiation(aglParser.AssignInstantiationContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignInstantiation}
	 * labeled alternative in {@link aglParser#assign}.
	 * @param ctx the parse tree
	 */
	void exitAssignInstantiation(aglParser.AssignInstantiationContext ctx);
	/**
	 * Enter a parse tree produced by the {@code instantiationDef}
	 * labeled alternative in {@link aglParser#instantiation}.
	 * @param ctx the parse tree
	 */
	void enterInstantiationDef(aglParser.InstantiationDefContext ctx);
	/**
	 * Exit a parse tree produced by the {@code instantiationDef}
	 * labeled alternative in {@link aglParser#instantiation}.
	 * @param ctx the parse tree
	 */
	void exitInstantiationDef(aglParser.InstantiationDefContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypeUnary}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypeUnary(aglParser.DataTypeUnaryContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypeUnary}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypeUnary(aglParser.DataTypeUnaryContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypePoint}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypePoint(aglParser.DataTypePointContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypePoint}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypePoint(aglParser.DataTypePointContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypeVector}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypeVector(aglParser.DataTypeVectorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypeVector}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypeVector(aglParser.DataTypeVectorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypeRealNumber}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypeRealNumber(aglParser.DataTypeRealNumberContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypeRealNumber}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypeRealNumber(aglParser.DataTypeRealNumberContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypeString}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypeString(aglParser.DataTypeStringContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypeString}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypeString(aglParser.DataTypeStringContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypeAction}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypeAction(aglParser.DataTypeActionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypeAction}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypeAction(aglParser.DataTypeActionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypeID}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypeID(aglParser.DataTypeIDContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypeID}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypeID(aglParser.DataTypeIDContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataTypeInteger}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void enterDataTypeInteger(aglParser.DataTypeIntegerContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataTypeInteger}
	 * labeled alternative in {@link aglParser#dataType}.
	 * @param ctx the parse tree
	 */
	void exitDataTypeInteger(aglParser.DataTypeIntegerContext ctx);
	/**
	 * Enter a parse tree produced by the {@code actionClose}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void enterActionClose(aglParser.ActionCloseContext ctx);
	/**
	 * Exit a parse tree produced by the {@code actionClose}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void exitActionClose(aglParser.ActionCloseContext ctx);
	/**
	 * Enter a parse tree produced by the {@code actionRefresh}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void enterActionRefresh(aglParser.ActionRefreshContext ctx);
	/**
	 * Exit a parse tree produced by the {@code actionRefresh}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void exitActionRefresh(aglParser.ActionRefreshContext ctx);
	/**
	 * Enter a parse tree produced by the {@code actionPrint}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void enterActionPrint(aglParser.ActionPrintContext ctx);
	/**
	 * Exit a parse tree produced by the {@code actionPrint}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void exitActionPrint(aglParser.ActionPrintContext ctx);
	/**
	 * Enter a parse tree produced by the {@code actionMouse}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void enterActionMouse(aglParser.ActionMouseContext ctx);
	/**
	 * Exit a parse tree produced by the {@code actionMouse}
	 * labeled alternative in {@link aglParser#action}.
	 * @param ctx the parse tree
	 */
	void exitActionMouse(aglParser.ActionMouseContext ctx);
	/**
	 * Enter a parse tree produced by the {@code figureDefinition}
	 * labeled alternative in {@link aglParser#figureDef}.
	 * @param ctx the parse tree
	 */
	void enterFigureDefinition(aglParser.FigureDefinitionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code figureDefinition}
	 * labeled alternative in {@link aglParser#figureDef}.
	 * @param ctx the parse tree
	 */
	void exitFigureDefinition(aglParser.FigureDefinitionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code viewDefinition}
	 * labeled alternative in {@link aglParser#viewDef}.
	 * @param ctx the parse tree
	 */
	void enterViewDefinition(aglParser.ViewDefinitionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code viewDefinition}
	 * labeled alternative in {@link aglParser#viewDef}.
	 * @param ctx the parse tree
	 */
	void exitViewDefinition(aglParser.ViewDefinitionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code loopDefinition}
	 * labeled alternative in {@link aglParser#loopDef}.
	 * @param ctx the parse tree
	 */
	void enterLoopDefinition(aglParser.LoopDefinitionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code loopDefinition}
	 * labeled alternative in {@link aglParser#loopDef}.
	 * @param ctx the parse tree
	 */
	void exitLoopDefinition(aglParser.LoopDefinitionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dataPointDef}
	 * labeled alternative in {@link aglParser#dataPoint}.
	 * @param ctx the parse tree
	 */
	void enterDataPointDef(aglParser.DataPointDefContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dataPointDef}
	 * labeled alternative in {@link aglParser#dataPoint}.
	 * @param ctx the parse tree
	 */
	void exitDataPointDef(aglParser.DataPointDefContext ctx);
}